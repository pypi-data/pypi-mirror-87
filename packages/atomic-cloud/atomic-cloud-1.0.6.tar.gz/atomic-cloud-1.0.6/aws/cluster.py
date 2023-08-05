from aws import cfm, ec2, region
from os import path
import boto3
import re
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass


###########################################################################
# Constants
###########################################################################

@dataclass
class _StackTypes:
    certificate = 'certificate'
    vpc = 'vpc'
    cp = 'cp'
    eks_workers = 'eks-workers'
    rds = 'rds'
    ecr = 'ecr'
    s3_storage = 's3-storage'
    s3_hosting = 's3-hosting'

STACK_TYPES = _StackTypes()

TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), 'templates')


###########################################################################
# Helper Functions
###########################################################################

def _abs_path(file_name: str):
    '''
    Helper function to get the absolute path for a template file in the cfm_templates directory.
    '''
    return path.join(TEMPLATE_DIR, 'cfm', file_name)


def _safe_domain(domain_name: str):
    '''
    Helper function to convert a domain to a safe resource name.
    All `.` will be replaced with `-`, and all non-alphanumeric characters (except `-`) will be stripped.
    '''
    return re.sub(r'[^a-zA-Z\d-]', '', domain_name.replace('.', '-'))


def _get_output(stack: dict, output_key: str):
    '''
    Helper function to get an OutputValue from the given stack
    '''
    return next((o['OutputValue'] for o in stack['Outputs'] if o.get('OutputKey') == output_key), None)


###########################################################################
# Wrapper Functions
###########################################################################

def create_cluster(vpc_name: str, vpc_class: str, domain_name: str, validation_domain: str = None, cidr_prefix: str = '10.10', workers: int = 2, db_password: str = 'postgres'):
    '''
    Create all cluster resource stacks. This is the preferred way of creating a cluster.

    Note, if this function is interrupted or raises an exception, the resources that were successfully created will remain in AWS.
    Call :meth:`~aws.cluster.delete_cluster` to cleanup these resources.

    :param vpc_name: The VPC name
    :param vpc_class: The VPC class (`np`, `prd`, or `cicd`). If `np` the `vpc_name` will be prepended to the domain (`vpcname.yourdomain.com`).
                      If `cicd`, `"cicd"` will be prepended to the domain (`cicd.yourdomain.com`). If `prd` the original domain will be used (`yourdomain.com`)
    :param domain_name: The domain name for which to request a certificate
    :param validation_domain: The suffix of the address to which validation emails will be sent. Must be the same as, or a superdomain of, `domain_name`. Defaults to `domain_name`
    :param cidr_prefix: The CIDR prefix. Default is `10.10`
    :param workers: The desired number of EKS workers. Default is 2.
    :param db_password: The database password. Default is `postgres`
    :return: A list of the created stacks
    '''
    stacks = []

    cert = create_certificate(vpc_name, vpc_class, domain_name, validation_domain=validation_domain)
    stacks.append(cert)

    if region.get_default_region() != 'us-east-1':
        with region.use_region('us-east-1'):
            east1_cert = create_certificate(vpc_name, vpc_class, domain_name, validation_domain=validation_domain)
            stacks.append(east1_cert)

    vpc = create_vpc(vpc_name, cidr_prefix=cidr_prefix)
    stacks.append(vpc)

    cp = create_cp(vpc_name)
    stacks.append(cp)

    eks_workers = create_eks_workers(vpc_name, workers)
    stacks.append(eks_workers)

    rds = create_rds(vpc_name, password=db_password)
    stacks.append(rds)

    return stacks


def delete_cluster(vpc_name: str, keep_certs=False):
    '''
    Delete all cluster resources.

    If you want to delete and recreate a cluster without re-approving certificates, the parameter `keep_certs` can be used.

    :param vpc_name: The VPC name
    :param keep_certs: If set, certificates will not be deleted
    :return: None
    '''
    delete_rds(vpc_name)
    delete_eks_workers(vpc_name)
    delete_cp(vpc_name)
    delete_vpc(vpc_name)
    if not keep_certs:
        delete_certificates(vpc_name)
        if region.get_default_region() != 'us-east-1':
            with region.use_region('us-east-1'):
                delete_certificates(vpc_name)


def create_app(vpc_name: str, app_name: str, domain_name: str, cicd_cross_account_number: str = None):
    '''
    Create all resources for a specific application. This is the preferred method.

    Note, if this function is interrupted or raises an exception, the resources that were successfully created will remain in AWS.
    Call :meth:`~aws.cluster.delete_app` to cleanup these resources.

    :param vpc_name: The VPC name
    :param app_name: The application name
    :param domain_name: The domain name
    :return: A list of the created stacks
    '''
    stacks = []

    ecr = create_ecr(app_name, cicd_cross_account_number=cicd_cross_account_number)
    stacks.append(ecr)

    s3_storage = create_s3_storage(vpc_name, app_name)
    stacks.append(s3_storage)

    s3_hosting = create_s3_hosting(vpc_name, app_name, domain_name)
    stacks.append(s3_hosting)

    return stacks


def delete_app(vpc_name: str, app_name: str):
    '''
    Delete all resources for a specific application.
    Will only delete ECR stack if no stacks for this app are found in other clusters.

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: None
    '''
    delete_s3_hosting(vpc_name, app_name)
    delete_s3_storage(vpc_name, app_name)

    dependant_stacks = cfm.find_stacks(AppName=app_name)
    if len(dependant_stacks) > 1: # (Account for the ECR stack itself)
        print(f'Skipping ECR deletion. Other clusters might still depend on it.')
    else:
        delete_ecr(app_name)


###########################################################################
# Certificate
###########################################################################

def create_certificate(vpc_name: str, vpc_class: str, domain_name: str, validation_domain: str = None):
    '''
    Create certificate stack.

    :param vpc_name: The VPC name
    :param vpc_class: The VPC class (`np`, `prd`, or `cicd`). If `np` the `vpc_name` will be prepended to the domain (`vpcname.yourdomain.com`).
                      If `cicd`, `"cicd"` will be prepended to the domain (`cicd.yourdomain.com`). If `prd` the original domain will be used (`yourdomain.com`)
    :param domain_name: The domain name for which to request a certificate.
    :param validation_domain: The suffix of the address to which validation emails will be sent. Must be the same as, or a superdomain of, `domain_name`. Defaults to `domain_name`
    :return: The created stack
    '''
    domain_safe = _safe_domain(domain_name)

    params = {
        'VpcClass': vpc_class,
        'VpcName': vpc_name or vpc_class,
        'DomainName': domain_name,
        'DomainSafe': domain_safe,
        'ValidationDomain': validation_domain or domain_name
    }

    tags = {
        'StackType': STACK_TYPES.certificate,
        'VpcName': vpc_name,
        'DomainName': domain_name,
    }

    message = {
        'np': f'Certificate requested for: `*.{vpc_name}.{domain_name}`, `*.sat.{domain_name}`, and `*.prf.{domain_name}`.',
        'prd': f'Certificate requested for: `*.{domain_name}`, `*.prd.{domain_name}`, and `*.trn.{domain_name}`.',
        'cicd': f'Certificate requested for: `*.cicd.{domain_name}`'
    }.get(vpc_class)
    if not message: raise ValueError(f'Unknown VpcClass: {vpc_class}')

    if not get_certificate(vpc_name, domain_name):
        print(message)
    else:
        print('Certificate already created, skipping request')

    return cfm.create_stack(_abs_path('00-cert.yml'), stack_name=f'{vpc_name}-00-cert-{domain_safe}', params=params, tags=tags)


def get_certificate(vpc_name: str, domain_name: str):
    '''
    Get certificate stack.

    :param vpc_name: The VPC name
    :param domain_name: The domain name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.certificate, VpcName=vpc_name, DomainName=domain_name)


def delete_certificate(vpc_name: str, domain_name: str):
    '''
    Delete certificate stack.

    :param vpc_name: The VPC name
    :param domain_name: The domain name
    :return: None
    '''
    cert = get_certificate(vpc_name, domain_name)
    if cert:
        cfm.delete_stack(cert.get('StackName'))


def delete_certificates(vpc_name: str):
    '''
    Delete all certificate stack for a cluster (vpc).

    :param vpc_name: The VPC name
    :return: None
    '''
    certs = cfm.find_stacks(StackType=STACK_TYPES.certificate, VpcName=vpc_name)
    for cert in certs:
        cfm.delete_stack(cert['StackName'])


###########################################################################
# VPC
###########################################################################

def create_vpc(vpc_name: str, cidr_prefix: str = '10.10'):
    '''
    Create VPC stack.

    :param vpc_name: The VPC name
    :param cidr_prefix: The CIDR prefix. Default is `10.10`
    :return: The created stack
    '''
    params = {
        'VpcName': vpc_name,
        'CidrPrefix': cidr_prefix,
        'azs': ec2.list_azs()
    }

    tags = {
        'StackType': STACK_TYPES.vpc,
        'VpcName': vpc_name
    }
    
    return cfm.create_stack(_abs_path('01-vpc.yml'), stack_name=f"{vpc_name}-01-vpc", params=params, tags=tags)


def get_vpc(vpc_name: str):
    '''
    Get VPC stack

    :param vpc_name: The VPC name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.vpc, VpcName=vpc_name)


def delete_vpc(vpc_name: str):
    '''
    Delete VPC stack.

    :param vpc_name: The VPC name
    :return: None
    '''
    vpc = cfm.find_stack(StackType=STACK_TYPES.vpc, VpcName=vpc_name)
    if vpc:
        cfm.delete_stack(vpc.get('StackName'))


###########################################################################
# Control Plane
###########################################################################

def create_cp(vpc_name: str):
    '''
    Create control plane stack. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param vpc_name: The VPC name
    :return: The created stack
    '''
    params = {
        'VpcName': vpc_name,
        'azs': ec2.list_azs()
    }

    tags = {
        'StackType': STACK_TYPES.cp,
        'VpcName': vpc_name
    }

    return cfm.create_stack(_abs_path('02-cp.yml'), stack_name=f"{vpc_name}-02-cp", params=params, capabilities=['CAPABILITY_NAMED_IAM'], tags=tags)


def get_cp(vpc_name: str):
    '''
    Get control plane stack

    :param vpc_name: The VPC name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.cp, VpcName=vpc_name)


def delete_cp(vpc_name: str):
    '''
    Delete control plane stack.

    :param vpc_name: The VPC name
    :return: None
    '''
    cp = cfm.find_stack(StackType=STACK_TYPES.cp, VpcName=vpc_name)
    if cp:
        cfm.delete_stack(cp.get('StackName'))


###########################################################################
# EKS Workers
###########################################################################

def create_eks_workers(vpc_name: str, workers: int = 2):
    '''
    Create EKS worker nodegroup stack. Must only be called after creating the control plane (:meth:`~aws.cluster.create_cp`)

    :param vpc_name: The VPC name
    :param workers: The desired number of workers. Default is 2.
    :return: The created stack
    '''
    params = {
        'VpcName': vpc_name,
        'Workers': workers
    }

    tags = {
        'StackType': STACK_TYPES.eks_workers,
        'VpcName': vpc_name
    }

    return cfm.create_stack(_abs_path('03-eks-workers.yml'), stack_name=f"{vpc_name}-03-eks-workers", params=params, capabilities=['CAPABILITY_NAMED_IAM'], tags=tags)


def get_eks_workers(vpc_name: str):
    '''
    Get EKS worker stack

    :param vpc_name: The VPC name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.eks_workers, VpcName=vpc_name)


def delete_eks_workers(vpc_name: str):
    '''
    Delete EKS worker stack.

    :param vpc_name: The VPC name
    :return: None
    '''
    eks_workers = cfm.find_stack(StackType=STACK_TYPES.eks_workers, VpcName=vpc_name)
    if eks_workers:
        cfm.delete_stack(eks_workers.get('StackName'))


###########################################################################
# RDS
###########################################################################

def create_rds(vpc_name: str, password: str = 'postgres', db_class: str = 'db.t2.micro', db_storage: int = 20):
    '''
    Create RDS stack. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param vpc_name: The VPC name
    :param password: The database password. Default is `postgres`
    :param db_class: The database instance class. Default is `db.t2.micro`. `Instance Classes <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html>`_
    :param db_storage: The allocated storage space in GBs. Default is 20
    :return: The created stack
    '''
    params = {
        'VpcName': vpc_name,
        'DBDefaultPassword': password,
        'DBClass': db_class,
        'DBStorage': db_storage
    }

    tags = {
        'StackType': STACK_TYPES.rds,
        'VpcName': vpc_name
    }

    return cfm.create_stack(_abs_path('04-rds.yml'), stack_name=f'{vpc_name}-04-rds', params=params, tags=tags)


def get_rds(vpc_name: str):
    '''
    Get RDS stack

    :param vpc_name: The VPC name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.rds, VpcName=vpc_name)


def delete_rds(vpc_name: str):
    '''
    Delete RDS stack

    :param vpc_name: The VPC name
    :return: None
    '''
    rds = cfm.find_stack(StackType=STACK_TYPES.rds, VpcName=vpc_name)
    if rds:
        cfm.delete_stack(rds.get('StackName'))


###########################################################################
# ECR
###########################################################################

def create_ecr(app_name: str, cicd_cross_account_number: str = None):
    '''
    Create ECR repository for an application. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param vpc_name: The VPC name
    :param app_name: The application name
    :param cicd_cross_account_number: The account number of the CICD environment if different from the current. Default is none.
    :return: The created stack
    '''
    params = {
        'AppName': app_name,
        'CicdCrossAccountNumber': cicd_cross_account_number
    }

    tags = {
        'StackType': STACK_TYPES.ecr,
        'AppName': app_name
    }

    return cfm.create_stack(_abs_path('ecr.yml'), stack_name=f'ecr-{app_name}', params=params, tags=tags)


def get_ecr(app_name: str):
    '''
    Get the ECR repository for an application

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.ecr, AppName=app_name)


def delete_ecr(app_name: str):
    '''
    Delete ECR stack

    :param app_name: The application name
    :return: None
    '''
    ecr = cfm.find_stack(StackType=STACK_TYPES.ecr, AppName=app_name)
    if ecr:
        cfm.delete_stack(ecr.get('StackName'))


###########################################################################
# S3 Storage
###########################################################################

def create_s3_storage(vpc_name: str, app_name: str):
    '''
    Create backend S3 storage for an application. Must only be called after creating the VPC (:meth:`~aws.cluster.create_vpc`)

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: The created stack
    '''
    if not cfm.stack_exists(f'{vpc_name}-01-vpc'):
        raise ValueError(f'VPC {vpc_name} does not exist')

    params = {
        'VpcName': vpc_name,
        'AppName': app_name
    }

    tags = {
        'StackType': STACK_TYPES.s3_storage,
        'VpcName': vpc_name,
        'AppName': app_name
    }

    return cfm.create_stack(_abs_path('s3-storage.yml'), stack_name=f'{vpc_name}-s3-storage-{app_name}', params=params, tags=tags)


def get_s3_storage(vpc_name: str, app_name: str):
    '''
    Get the S3 storage bucket for an application
    
    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: The discovered stack if found, else None
    '''
    return cfm.find_stack(StackType=STACK_TYPES.s3_storage, VpcName=vpc_name, AppName=app_name)


def delete_s3_storage(vpc_name: str, app_name: str):
    '''
    Delete S3 storage stack

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: None
    '''
    s3_storage = cfm.find_stack(StackType=STACK_TYPES.s3_storage, VpcName=vpc_name, AppName=app_name)
    if s3_storage:
        cfm.delete_stack(s3_storage.get('StackName'))
        bucket = _get_output(s3_storage, 'Bucket')
        if bucket:
            region.get_s3().delete_bucket(Bucket=bucket)


###########################################################################
# S3 Hosting
###########################################################################

def create_s3_hosting(vpc_name: str, app_name: str, domain_name: str):
    '''
    Create hosting resources for an application (S3 bucket and CloudFront distribution).
    
    Must only be called after creating a certificate for the given domain (:meth:`~aws.cluster.create_certificate`).
    Note: The certificate in question must be created in the us-east-1 region regardless of the region where the cluster resides.

    :param vpc_name: The VPC name
    :param app_name: The application name
    :param domain_name: The domain name
    :return: The created stack
    '''
    if not cfm.stack_exists(f'{vpc_name}-01-vpc'):
        raise ValueError(f'VPC {vpc_name} does not exist')

    with region.use_region('us-east-1'):
        cert = get_certificate(vpc_name, domain_name)

    if not cert:
        raise Exception(f'Certificate not found for {domain_name} in us-east-1. Must call create_certificate() in us-east-1 region before proceding.')

    params = {
        'VpcName': vpc_name,
        'AppName': app_name,
        'DomainName': domain_name,
        'DomainSafe': _safe_domain(domain_name),
        'CertArn': _get_output(cert, 'OutputCertificate')
    }

    tags = {
        'StackType': STACK_TYPES.s3_hosting,
        'VpcName': vpc_name,
        'AppName': app_name,
        'DomainName': domain_name
    }

    return cfm.create_stack(_abs_path('s3-hosting.yml'), stack_name=f'{vpc_name}-s3-hosting-{app_name}', params=params, tags=tags)


def get_s3_hosting(vpc_name: str, app_name: str):
    '''
    Get the hosting resources for an application (S3 bucket and CloudFront distribution)

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: The created stack
    '''
    return cfm.find_stack(StackType=STACK_TYPES.s3_hosting, VpcName=vpc_name, AppName=app_name)


def delete_s3_hosting(vpc_name: str, app_name: str):
    '''
    Delete hosting stack

    :param vpc_name: The VPC name
    :param app_name: The application name
    :return: None
    '''
    hosting = cfm.find_stack(StackType=STACK_TYPES.s3_hosting, VpcName=vpc_name, AppName=app_name)
    if hosting:
        cfm.delete_stack(hosting.get('StackName'))
        bucket = _get_output(hosting, 'Bucket')
        if bucket:
            region.get_s3().delete_bucket(Bucket=bucket)


###########################################################################
# Factsheets
###########################################################################

def generate_cluster_factsheet(vpc_name: str, output_dir: str = '.'):
    '''
    Create factsheet for a cluster.

    :param vpc_name: The VPC name
    :param output_dir: The target directory for the factsheet file. Defaults to current working directory
    :return: None
    '''
    print(f'Generating cluster factsheet for {vpc_name}...')

    params = {}

    params['VpcName'] = vpc_name
    params['account'] = region.get_account_id()
    account_aliases = region.get_iam().list_account_aliases()['AccountAliases']
    params['accountAlias'] = account_aliases[0] if account_aliases else None
    params['region'] = region.get_session_region()
    params['azs'] = ec2.list_azs()

    vpc = get_vpc(vpc_name)
    params['vpcId'] = _get_output(vpc, 'VPC')
    cidr_range = _get_output(vpc, 'CidrRange')
    params['cidrBase'] = re.findall(r'\d+\.\d+', cidr_range)[0]

    private_subnets = _get_output(vpc, 'PrivateSubnets').split(',')
    private_subnets.insert(1, None)
    private_subnets.insert(4, None)
    params['subPrivateIds'] = private_subnets

    public_subnets = _get_output(vpc, 'PublicSubnets').split(',')
    public_subnets.insert(1, None)
    public_subnets.insert(4, None)
    params['subPublicIds'] = public_subnets

    cp = get_cp(vpc_name)
    params['cpName'] = _get_output(cp, 'Cluster')
    params['cpArn'] = _get_output(cp, 'ARN')
    params['sgMasterId'] = _get_output(cp, 'SecurityGroup')
    params['sgNodesId'] = _get_output(cp, 'SharedNodeSecurityGroup')
    params['cpRoleArn'] = _get_output(cp, 'ServiceRoleARN')

    eks_workers = get_eks_workers(vpc_name)
    params['ngName'] = _get_output(eks_workers, 'NodegroupName')
    params['ngArn'] = _get_output(eks_workers, 'NodegroupArn')
    params['nodeRoleArn'] = _get_output(eks_workers, 'NodeRoleArn')

    rds = get_rds(vpc_name)
    params['rdsName'] = _get_output(rds, 'DBInstance')
    params['rdsHost'] = _get_output(rds, 'DBHostName')

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), lstrip_blocks=True, trim_blocks=True)
    template = env.get_template('factsheet/cluster-factsheet.md')
    filename = f'{vpc_name}-factsheet.md'
    template.stream(params).dump(path.join(output_dir, filename))
    return filename


def generate_app_factsheet(vpc_names: list, app_name: str, output_dir: str = '.'):
    '''
    Create factsheet for a cluster.

    :param vpc_names: List of VPC names for the application
    :param app_name: The application name
    :param output_dir: The target directory for the factsheet file. Defaults to current working directory
    :return: None
    '''
    print(f'Generating application factsheet for {app_name}...')

    def get_resources(vpc_name, app_name):
        'Get app resources by vpc'
        s3_storage = get_s3_storage(vpc_name, app_name)
        s3_storage_bucket = _get_output(s3_storage, 'Bucket')
        hosting = get_s3_hosting(vpc_name, app_name)
        s3_host_bucket = _get_output(hosting, 'Bucket')
        cf_dist = _get_output(hosting, 'Distribution')
        return (s3_storage_bucket, s3_host_bucket, cf_dist)

    params = {
        'app_name': app_name,
        'account': region.get_account_id(),
        'account_alias': region.get_account_alias(),
        'region': region.get_session_region(),
        'ecr_repo': _get_output(get_ecr(app_name), 'Repository'),
        'resources_by_vpc': {vpc_name: get_resources(vpc_name, app_name) for vpc_name in vpc_names}
    }

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), lstrip_blocks=True, trim_blocks=True)
    template = env.get_template('factsheet/app-factsheet.md')
    filename = f'{app_name}-factsheet.md'
    template.stream(params).dump(path.join(output_dir, filename))
    return filename