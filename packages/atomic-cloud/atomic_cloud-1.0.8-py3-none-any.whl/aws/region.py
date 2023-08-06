import boto3
import contextlib

###########################################################################
# Region
###########################################################################
_region = boto3.session.Session().region_name or 'us-east-1'


@contextlib.contextmanager
def use_region(region: str):
    """
    Simple context manager which allows temporarily setting the default region using a `with` statement.

    Example usage::

        set_default_region('us-east-2')
        # Perform actions in us-east-2...
        
        with use_region('us-east-1'):
            # Temporarily perform actions in us-east-1...

        # Resume performing actions in us-east-2...
    
    :param region: The region to temporarily use
    :return: None
    """
    try:
        default_region = get_default_region()
        set_default_region(region)
        yield
    finally:
        set_default_region(default_region)


def set_default_region(region: str):
    """
    Initializes all library clients based on the specified region.  The library clients
    are AWS API clients that give us access to AWS.  Note that if you set the region with
    **aws configure**, that will take precedence.

    :param region: The region that all library clients will be opened with.
    :return: No return value.
    """
    global _region
    _region = region


def get_default_region():
    """
    :return: The default region all clients are using. Note that if you set the region with aws configure, that region takes precedence over this one.
    """
    global _region
    return _region


def get_session_region():
    """
    Used to get the region on a device/account where aws-configure has been used to set the region.
    :return: the region this session is using.
    """
    return boto3.session.Session().region_name


def get_account_id():
    """
    :return: the account ID of the instance/user/identity executing the script as a string
    """
    return str(boto3.client('sts').get_caller_identity().get('Account'))


def get_account_alias():
    """
    :return: the alias of the account id returned by `get_account_id()` if it exists, else None
    """
    account_aliases = get_iam().list_account_aliases()['AccountAliases']
    return account_aliases[0] if account_aliases else None


def get_ec2():
    """
    :return: An EC2 client using the default region.
    """
    return boto3.client('ec2', _region)


def get_ecs():
    """
    :return: An ECS client using the default region.
    """
    return boto3.client('ecs', _region)


def get_elb():
    """
    :return: An Elastic Load Balancer client using the default region.
    """
    return boto3.client('elb', _region)


def get_elbv2():
    """
    :return: An Elastic Load Balancer V2 client using the default region.
    """
    return boto3.client('elbv2', _region)


def get_iam():
    """
    :return: An IAM client using the default region.
    """
    return boto3.client('iam', _region)


def get_rds():
    """
    :return: A RDS client using the default region.
    """
    return boto3.client('rds', _region)


def get_ssm():
    """
    :return: A Secure Systems Manager client using the default region.
    """
    return boto3.client('ssm', _region)


def get_secret():
    """
    :return: A Secrets Manager client using the default region.
    """
    return boto3.client('secretsmanager', _region)


def get_route53():
    """
    :return: A Route53 client.
    """
    return boto3.client('route53')


def get_acm():
    """
    :return: A Certificate Manager client;
    """
    return boto3.client('acm', _region)


def get_cloudformation():
    """
    :return: A CloudFormation client
    """
    return boto3.client('cloudformation', _region)


def get_s3():
    """
    :return: An S3 client
    """
    return boto3.client('s3', _region)