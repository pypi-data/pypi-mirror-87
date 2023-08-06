from unittest import TestCase, main
from aws import cluster, cfm, ec2
import boto3
import warnings
import os
from dataclasses import dataclass


@dataclass
class _Config:
    '''All the test parameters'''
    vpc_name = 'ac-unit-test'
    vpc_class = 'np'
    domain_name = 'ac-unit-test.simoncomputing.com'
    validation_domain = 'simoncomputing.com'
    cidr_prefix = '10.10'
    workers = 2
    db_password = 'password'
    app_name = 'ac-unit-test-app'

CONFIG = _Config()


def create_test_cluster():
    '''
    This can be used externally to create the test cluster before running tests.
    Useful for reusing the resources created here in other test files.
    '''
    try:
        cluster.create_cluster(CONFIG.vpc_name, CONFIG.vpc_class, CONFIG.domain_name,
                            validation_domain=CONFIG.validation_domain,
                            cidr_prefix=CONFIG.cidr_prefix,
                            workers=CONFIG.workers,
                            db_password=CONFIG.db_password) 
        cluster.create_app(CONFIG.vpc_name, CONFIG.app_name, CONFIG.domain_name)
    except Exception as e:
        print('Exception raised during cluster creation. Cleaning up created resources...')
        delete_test_cluster()
        raise e


def delete_test_cluster():
    cluster.delete_app(CONFIG.vpc_name, CONFIG.app_name)
    cluster.delete_cluster(CONFIG.vpc_name, keep_certs=True)


def get_output(stack: dict, output_key: str):
    '''Helper function to get an OutputValue from the given stack'''
    return next((o['OutputValue'] for o in stack['Outputs'] if o.get('OutputKey') == output_key), None)


class TestCluster(TestCase):

    ###########################################################################
    # Test Setup/Cleanup
    ###########################################################################

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)
        
        # NOTE: If running this test standalone, uncomment this line
        # create_test_cluster()


    @classmethod
    def tearDownClass(cls):
        # NOTE: If running this test standalone, uncomment this line
        # delete_test_cluster()
        pass


    ###########################################################################
    # Certificate
    ###########################################################################

    def test_create_certificate_invalid_vpc_class(self):
        with self.assertRaises(ValueError):
            cluster.create_certificate(CONFIG.vpc_name, 'garbage', CONFIG.domain_name, validation_domain=CONFIG.validation_domain)
    

    def test_create_certificate_invalid_domain_name(self):
        with self.assertRaises(Exception):
            cert = cluster.create_certificate(CONFIG.vpc_name, CONFIG.vpc_class, 'garbage', validation_domain=CONFIG.validation_domain)
            cfm.delete_stack(cert['StackName'])

    
    def test_create_certificate(self):
        cert = cluster.create_certificate(CONFIG.vpc_name, CONFIG.vpc_class, CONFIG.domain_name, validation_domain=CONFIG.validation_domain)
        
        cert_arn = get_output(cert, 'OutputCertificate')
        self.assertIsNotNone(cert_arn, msg='Certificate ARN not found in output')

        try:
            boto3.client('acm').get_certificate(CertificateArn=cert_arn)
        except Exception:
            self.fail(f'Could not find certificate with ARN: {cert_arn}. It may have not been created properly.')


    def test_get_certificate_nonexistent(self):
        cert = cluster.get_certificate('bogus', 'garbage')
        self.assertIsNone(cert)


    def test_get_certificate(self):
        cert = cluster.get_certificate(CONFIG.vpc_name, CONFIG.domain_name)
        self.assertIsNotNone(cert)


    ###########################################################################
    # VPC
    ###########################################################################

    def test_create_vpc_invalid_cidr(self):
        with self.assertRaises(Exception):
            stack = cluster.create_vpc('bogus', cidr_prefix='garbage')
            cfm.delete_stack(stack['StackName']) 


    def test_create_vpc(self):
        vpc = cluster.create_vpc(CONFIG.vpc_name, cidr_prefix=CONFIG.cidr_prefix)
        
        vpcid = get_output(vpc, 'VPC')
        self.assertIsNotNone(ec2.get_vpc(vpcid=vpcid))


    def test_get_vpc_nonexistent(self):
        vpc = cluster.get_vpc('garbage')
        self.assertIsNone(vpc)


    def test_get_vpc(self):
        vpc = cluster.get_vpc(CONFIG.vpc_name)
        self.assertIsNotNone(vpc)


    ###########################################################################
    # CP
    ###########################################################################
    
    def test_create_cp_unknown_vpc(self):
        with self.assertRaises(Exception):
            cp = cluster.create_cp('garbage')
            cfm.delete_stack(cp['StackName'])
    
    
    def test_create_cp(self):
        cp = cluster.create_cp(CONFIG.vpc_name)

        cluster_name = get_output(cp, 'Cluster')

        try:
            boto3.client('eks').describe_cluster(name=cluster_name)
        except Exception:
            self.fail(f'Could not find cluster: {cluster_name}. It may not have been created properly.')


    def test_get_cp_nonexistent(self):
        cp = cluster.get_cp('garbage')
        self.assertIsNone(cp)


    def test_get_cp(self):
        cp = cluster.get_cp(CONFIG.vpc_name)
        self.assertIsNotNone(cp)


    ###########################################################################
    # EKS Workers
    ###########################################################################

    def test_create_eks_workers_unknown_cp(self):
        with self.assertRaises(Exception):
            eks_workers = cluster.create_eks_workers('garbage', CONFIG.workers)
            cfm.delete_stack(eks_workers['StackName'])


    def test_create_eks_workers(self):
        eks_workers = cluster.create_eks_workers(CONFIG.vpc_name, CONFIG.workers)

        cluster_name = get_output(eks_workers, 'ClusterName')
        nodegroup_name = get_output(eks_workers, 'NodegroupName')

        try:
            boto3.client('eks').describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
        except Exception:
            self.fail(f'Could not find nodegroup: {nodegroup_name}. It may not have been created properly.')


    def test_get_eks_workers_nonexistent(self):
        workers = cluster.get_eks_workers('garbage')
        self.assertIsNone(workers)


    def test_get_eks_workers(self):
        eks_workers = cluster.get_eks_workers(CONFIG.vpc_name)
        self.assertIsNotNone(eks_workers)


    ###########################################################################
    # RDS
    ###########################################################################
    
    def test_create_rds_unknown_vpc(self):
        with self.assertRaises(Exception):
            rds = cluster.create_rds('garbage')
            cfm.delete_stack(rds['StackName'])


    def test_create_rds(self):
        rds = cluster.create_rds(CONFIG.vpc_name, password=CONFIG.db_password)

        instance_id = get_output(rds, 'DBInstance')

        try:
            boto3.client('rds').describe_db_instances(DBInstanceIdentifier=instance_id)
        except Exception:
            self.fail(f'Could not find RDS instance: {instance_id}. It may not have been created properly.')


    def test_get_rds_nonexistent(self):
        rds = cluster.get_rds('garbage')
        self.assertIsNone(rds)


    def test_get_rds(self):
        rds = cluster.get_rds(CONFIG.vpc_name)
        self.assertIsNotNone(rds)


    ###########################################################################
    # ECR
    ###########################################################################
    
    def test_create_ecr(self):
        ecr = cluster.create_ecr(CONFIG.app_name)

        repo_name = get_output(ecr, 'Repository')

        try:
            boto3.client('ecr').describe_repositories(repositoryNames=[repo_name])
        except Exception:
            self.fail(f'Could not find ECR repository: {repo_name}. It may not have been created properly')


    def test_get_ecr_nonexistent(self):
        ecr = cluster.get_ecr('garbage')
        self.assertIsNone(ecr)


    def test_get_ecr(self):
        ecr = cluster.get_ecr(CONFIG.app_name)
        self.assertIsNotNone(ecr)


    ###########################################################################
    # S3 Storage
    ###########################################################################

    def test_create_s3_storage_unknown_vpc(self):
        with self.assertRaises(ValueError):
            s3_storage = cluster.create_s3_storage('garbage', CONFIG.app_name)
            cfm.delete_stack(s3_storage['StackName'])


    def test_create_s3_storage(self):
        s3_storage = cluster.create_s3_storage(CONFIG.vpc_name, CONFIG.app_name)

        bucket = get_output(s3_storage, 'Bucket')

        try:
            boto3.client('s3').list_objects(Bucket=bucket)
        except Exception:
            self.fail(f'Could not find bucket {bucket}. It may not have been created properly.')


    def test_get_s3_storage_nonexistent(self):
        s3_storage = cluster.get_s3_storage('bogus', 'garbage')
        self.assertIsNone(s3_storage)


    def test_get_s3_storage(self):
        s3_storage = cluster.get_s3_storage(CONFIG.vpc_name, CONFIG.app_name)
        self.assertIsNotNone(s3_storage)


    ###########################################################################
    # S3 Hosting
    ###########################################################################
    
    def test_create_s3_hosting_unknown_vpc(self):
        with self.assertRaises(ValueError):
            s3_hosting = cluster.create_s3_hosting('garbage', CONFIG.app_name, CONFIG.domain_name)
            cfm.delete_stack(s3_hosting['StackName'])


    def test_create_s3_hosting_no_cert(self):
        with self.assertRaises(Exception):
            s3_hosting = cluster.create_s3_hosting(CONFIG.vpc_name, CONFIG.app_name, 'domain.with.no.certificate')
            cfm.delete_stack(s3_hosting['StackName'])


    def test_create_s3_hosting(self):
        s3_hosting = cluster.create_s3_hosting(CONFIG.vpc_name, CONFIG.app_name, CONFIG.domain_name)

        bucket = get_output(s3_hosting, 'Bucket')

        try:
            boto3.client('s3').list_objects(Bucket=bucket)
        except Exception:
            self.fail(f'Could not find bucket {bucket}. It may not have been created properly.')

        distribution = get_output(s3_hosting, 'Distribution')

        try:
            boto3.client('cloudfront').get_distribution(Id=distribution)
        except Exception:
            self.fail(f'Could not find cloudfront distribution {distribution}. It may not have been created properly.')


    def test_get_s3_hosting_nonexistent(self):
        s3_hosting = cluster.get_s3_hosting('bogus', 'garbage')
        self.assertIsNone(s3_hosting)


    def test_get_s3_hosting(self):
        s3_hosting = cluster.get_s3_hosting(CONFIG.vpc_name, CONFIG.app_name)
        self.assertIsNotNone(s3_hosting)


    ###########################################################################
    # Cluster Factsheet
    ###########################################################################

    def test_generate_cluster_factsheet_nonexistent_vpc(self):
        with self.assertRaises(Exception):
            cluster.generate_cluster_factsheet('garbage')
    

    def test_generate_cluster_factsheet(self):
        filename = cluster.generate_cluster_factsheet(CONFIG.vpc_name)
        self.assertTrue(os.path.isfile(filename))

    
    ###########################################################################
    # App Factsheet
    ###########################################################################

    def test_generate_app_factsheet_nonexistent_app(self):
        with self.assertRaises(Exception):
            cluster.generate_app_factsheet(['bogus'], 'garbage')


    def test_generate_app_factsheet(self):
        filename = cluster.generate_app_factsheet([CONFIG.vpc_name], CONFIG.app_name)
        self.assertTrue(os.path.isfile(filename))


if __name__ == "__main__":
    main()