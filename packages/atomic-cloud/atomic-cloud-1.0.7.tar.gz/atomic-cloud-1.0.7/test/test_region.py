import unittest
from aws import region
import boto3
import warnings


class TestRegion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', category=ResourceWarning)


    ###########################################################################
    # Default Region
    ###########################################################################

    def test_set_default_region(self):
        region.set_default_region('us-east-2')
        self.assertEqual(region._region, 'us-east-2')


    def test_get_default_region(self):
        self.assertEqual(region.get_default_region(), boto3.session.Session().region_name)


    def test_get_session_region(self):
        self.assertEqual(region.get_session_region(), boto3.session.Session().region_name)


    def test_use_region(self):
        region.set_default_region('us-east-1')
        self.assertEqual(region.get_default_region(), 'us-east-1')

        with region.use_region('us-east-2'):
            self.assertEqual(region.get_default_region(), 'us-east-2')

        self.assertEqual(region.get_default_region(), 'us-east-1')


    ###########################################################################
    # Account Information
    ###########################################################################

    def test_get_account_id(self):
        self.assertIsNotNone(region.get_account_id())


    def test_get_account_alias(self):
        self.assertIsNotNone(region.get_account_alias())


    ###########################################################################
    # Clients
    ###########################################################################

    def test_get_ec2(self):
        client = region.get_ec2()
        response = client.describe_availability_zones()
        self.assertIsNotNone(response)

    
    def test_get_ecs(self):
        client = region.get_ecs()
        response = client.describe_clusters()
        self.assertIsNotNone(response)


    def test_get_elb(self):
        client = region.get_elb()
        response = client.describe_load_balancers()
        self.assertIsNotNone(response)


    def test_get_elbv2(self):
        client = region.get_elbv2()
        response = client.describe_load_balancers()
        self.assertIsNotNone(response)


    def test_get_iam(self):
        client = region.get_iam()
        response = client.list_account_aliases()
        self.assertIsNotNone(response)


    def test_get_rds(self):
        client = region.get_rds()
        response = client.describe_db_instances()
        self.assertIsNotNone(response)


    def test_get_ssm(self):
        client = region.get_ssm()
        response = client.list_commands()
        self.assertIsNotNone(response)


    def test_get_secret(self):
        client = region.get_secret()
        response = client.list_secrets()
        self.assertIsNotNone(response)


    def test_get_route53(self):
        client = region.get_route53()
        response = client.list_hosted_zones()
        self.assertIsNotNone(response)


    def test_get_acm(self):
        client = region.get_acm()
        response = client.list_certificates()
        self.assertIsNotNone(response)


    def test_get_cloudformation(self):
        client = region.get_cloudformation()
        response = client.list_stacks()
        self.assertIsNotNone(response)


    def test_get_s3(self):
        client = region.get_s3()
        response = client.list_buckets()
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main(verbosity=2)