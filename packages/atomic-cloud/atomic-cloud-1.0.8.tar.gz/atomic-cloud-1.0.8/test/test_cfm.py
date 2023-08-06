import unittest
import os
import warnings
from aws import cfm, ec2


VPC_NAME = 'cfm-unit-test'


def _abs_path(file: str):
    basedir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, file)


def stack_matches(found, expected):
    return found['StackName'] == expected['StackName']


def stack_found(stack, stacks):
    return any( s for s in stacks if stack_matches(s, stack) )


class TestCloudFormation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        params = {
            'VpcName': VPC_NAME,
            'CidrPrefix': '10.10'
        }

        cls.STACK_NAME = f'{VPC_NAME}-basic-stack'
        cls.STACK = cfm.create_stack(
            _abs_path('templates/basic-stack.yaml'),
            stack_name=cls.STACK_NAME,
            params=params,
            capabilities=[cfm.CAPABILITY_NAMED_IAM],
            tags={'VpcName': VPC_NAME},
            debug=True)


    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(cls.STACK_NAME)


    ###########################################################################
    # List Stacks
    ###########################################################################

    def test_list_stacks(self):
        all_stacks = cfm.list_stacks()
        self.assertTrue(stack_found(self.STACK, all_stacks))

        completed_stacks = cfm.list_stacks(stack_status_filter=cfm.CREATE_COMPLETE)
        self.assertTrue(stack_found(self.STACK, completed_stacks))


    def test_list_stacks_bogus_filter(self):
        stacks = cfm.list_stacks(stack_status_filter='bogus')
        self.assertEqual(stacks, [])


    ###########################################################################
    # Describe Stacks
    ###########################################################################

    def test_describe_stacks(self):
        all_stacks = cfm.describe_stacks()
        self.assertTrue(stack_found(self.STACK, all_stacks))

        filtered_stacks = cfm.describe_stacks(stack_name=self.STACK_NAME)
        self.assertTrue(stack_found(self.STACK, filtered_stacks))


    def test_describe_stacks_bogus_filter(self):
        stacks = cfm.describe_stacks(stack_name='bogus')
        self.assertEqual(stacks, [])


    ###########################################################################
    # Find Stacks
    ###########################################################################

    def test_find_stacks_exact_match(self):
        stacks = cfm.find_stacks(VpcName=VPC_NAME)
        self.assertTrue(stack_found(self.STACK, stacks))

        stacks = cfm.find_stacks(BogusTag='garbage')
        self.assertEqual(stacks, [])

        stacks = cfm.find_stacks(VpcName=VPC_NAME, BogusTag='garbage')
        self.assertEqual(stacks, [])

    
    def test_find_stacks_loose_match(self):
        stacks = cfm.find_stacks(match_all=False, VpcName=VPC_NAME)
        self.assertTrue(stack_found(self.STACK, stacks))

        stacks = cfm.find_stacks(match_all=False, BogusTag='garbage')
        self.assertEqual(stacks, [])

        stacks = cfm.find_stacks(match_all=False, VpcName=VPC_NAME, BogusTag='garbage')
        self.assertTrue(stack_found(self.STACK, stacks))


    ###########################################################################
    # Find Stack
    ###########################################################################

    def test_find_stack_exact_match(self):
        stack = cfm.find_stack(VpcName=VPC_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))

        stack = cfm.find_stack(BogusTag='garbage')
        self.assertIsNone(stack)

        stack = cfm.find_stack(VpcName=VPC_NAME, BogusTag='garbage')
        self.assertIsNone(stack)


    def test_find_stack_loose_match(self):
        stack = cfm.find_stack(match_all=False, VpcName=VPC_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))

        stack = cfm.find_stack(match_all=False,BogusTag='garbage')
        self.assertIsNone(stack)

        stack = cfm.find_stack(match_all=False, VpcName=VPC_NAME, BogusTag='garbage')
        self.assertTrue(stack_matches(stack, self.STACK))


    ###########################################################################
    # Stack Status
    ###########################################################################

    def test_get_stack_status(self):
        status = cfm.get_stack_status(self.STACK_NAME)
        self.assertEqual(status, cfm.CREATE_COMPLETE)


    def test_get_stack_status_bogus_stack(self):
        status = cfm.get_stack_status('bogus')
        self.assertIsNone(status)


    ###########################################################################
    # Get Stack
    ###########################################################################

    def test_get_stack(self):
        stack = cfm.get_stack(self.STACK_NAME)
        self.assertTrue(stack_matches(stack, self.STACK))


    def test_get_stack_bogus_name(self):
        stack = cfm.get_stack('bogus')
        self.assertIsNone(stack)


    ###########################################################################
    # Stack Exists
    ###########################################################################    

    def test_stack_exists(self):
        exists = cfm.stack_exists(self.STACK_NAME)
        self.assertTrue(exists)


    def test_stack_exists_bogus_name(self):
        exists = cfm.stack_exists('bogus')
        self.assertFalse(exists)


    ###########################################################################
    # Wait For Stack
    ###########################################################################

    def test_wait_for_stack(self):
        status = cfm.wait_for_stack(self.STACK_NAME, cfm.CREATE_IN_PROGRESS)
        self.assertEqual(status, cfm.CREATE_COMPLETE)


    ###########################################################################
    # Create Stack
    ###########################################################################

    # NOTE: Happy path tested via tes setup and other functions

    def test_create_stack_default_name(self):
        # The autogenerated name should match the existing stack name
        # Creation should be skipped and the existing stack returned:
        stack = cfm.create_stack(_abs_path('templates/basic-stack.yaml'), params={'VpcName': VPC_NAME})
        self.assertEqual(stack, self.STACK)


    def test_create_stack_already_exists(self):
        existing = cfm.create_stack(_abs_path('templates/basic-stack.yaml'), stack_name=self.STACK_NAME)
        self.assertEqual(existing, self.STACK)


    def test_create_stack_bogus_filename(self):
        result = cfm.create_stack('bogus', stack_name='garbage')
        self.assertIsNone(result)


    ###########################################################################
    # Get Export Value
    ###########################################################################

    def test_get_export_value(self):
        export_name = f'{VPC_NAME}-vpc'
        export_value = cfm.get_export_value(self.STACK_NAME, export_name)
        self.assertIsNotNone(export_value)


    def test_get_export_value_bogus_export(self):
        export_value = cfm.get_export_value(self.STACK_NAME, 'bogus')
        self.assertIsNone(export_value)


    def test_get_export_value_bogus_stack(self):
        export_name = f'{VPC_NAME}-vpc'
        export_value = cfm.get_export_value('bogus', export_name)
        self.assertIsNone(export_value)


    ###########################################################################
    # Delete Stack
    ###########################################################################

    # NOTE: Happy path tested via tear down function

    def test_delete_stack_bogus_stack(self):
        status = cfm.delete_stack('bogus')
        self.assertIsNone(status)


    ###########################################################################
    # Get Output
    ###########################################################################

    def test_get_output(self):
        output = cfm.get_output(self.STACK, 'VPC')
        self.assertIsNotNone(output)

        output = cfm.get_output(self.STACK_NAME, 'VPC')
        self.assertIsNotNone(output)


    def test_get_output_bogus_stack(self):
        with self.assertRaises(Exception):
            cfm.get_output(['wrong-type'], 'VPC')
        with self.assertRaises(Exception):
            cfm.get_output({}, 'VPC')
    
    
    def test_get_output_bogus_output(self):
        output = cfm.get_output(self.STACK, 'bogus')
        self.assertIsNone(output)


    ###########################################################################
    # Get Resources
    ###########################################################################

    def test_get_resources(self):
        resources = cfm.get_resources(self.STACK_NAME)
        self.assertNotEqual(resources, [])

    
    def test_get_resources_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resources('bogus')


    def test_get_resource(self):
        resource = cfm.get_resource(self.STACK_NAME, 'VPC')
        self.assertIsNotNone(resource)


    def test_get_resource_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resource('bogus', 'VPC')

    
    def test_get_resource_bogus_resource(self):
        resource = cfm.get_resource(self.STACK_NAME, 'bogus')
        self.assertIsNone(resource)


    def test_get_resource_id(self):
        resource_id = cfm.get_resource_id(self.STACK_NAME, 'VPC')
        vpc = ec2.get_vpc(vpcid=resource_id)
        self.assertIsNotNone(vpc)


    def test_get_resource_id_bogus_stack(self):
        with self.assertRaises(ValueError):
            cfm.get_resource_id('bogus', 'VPC')


    def test_get_resource_id_bogus_resource(self):
        resource_id = cfm.get_resource_id(self.STACK_NAME, 'bogus')
        self.assertIsNone(resource_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)