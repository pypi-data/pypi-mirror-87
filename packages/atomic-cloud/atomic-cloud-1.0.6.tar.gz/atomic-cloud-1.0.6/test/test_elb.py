from aws import elb, cfm, ec2, region
import unittest
import warnings
from os import path


IDENTIFIER = 'test-elb'

VPC_STACK = None
VPC = None
BASTION_STACK = None


def _abs_path(file: str):
    basedir = path.abspath(path.dirname(__file__))
    return path.join(basedir, file)


class TestELB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        parameters = {
            'EnvType': IDENTIFIER,
            'CidrPrefix': '10.222',
            'DomainName': f'{IDENTIFIER}.simoncomputing.com',
            'KeyName': f'{IDENTIFIER}-key-pair',
            'azs': ec2.list_azs()
        }

        if not ec2.key_pair_exists(parameters['KeyName']):
            ec2.create_key_pair(parameters['KeyName'])

        global VPC, VPC_STACK, BASTION_STACK
        VPC_STACK = f'{IDENTIFIER}-rancher-vpc'
        cfm.create_stack(_abs_path('templates/rancher-vpc.yaml'), stack_name=VPC_STACK, params=parameters)
        VPC = ec2.get_vpc(vpcid=cfm.get_resource_id(VPC_STACK, 'RancherVpc'))
        BASTION_STACK = f'{IDENTIFIER}-rancher-bastion'
        cfm.create_stack(_abs_path('templates/rancher-bastion.yaml'), stack_name=BASTION_STACK, params=parameters)


    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(BASTION_STACK)
        cfm.delete_stack(VPC_STACK)
        ec2.delete_key_pair(f'{IDENTIFIER}-key-pair')


    ###########################################################################
    # Classic Load Balancer
    ###########################################################################

    def test_list_classic_loadbalancer(self):
        lbs = elb.list_classic_loadbalancer()
        lb_name = cfm.get_resource_id(VPC_STACK, 'ClassicLoadBalancer')
        found = [ lb['LoadBalancerName'] for lb in lbs if lb['LoadBalancerName'] == lb_name ]
        self.assertNotEqual(found, [])


    def test_get_class_loadbalancer(self):
        lb_name = cfm.get_resource_id(VPC_STACK, 'ClassicLoadBalancer')
        lb = elb.get_classic_loadbalancer(lb_name)
        self.assertIsNotNone(lb)


    def test_get_class_loadbalancer_nonexistent(self):
        lb = elb.get_classic_loadbalancer('bogus')
        self.assertIsNone(lb)


    def test_get_class_loadbalancer_fail(self):
        with self.assertRaises(Exception):
            elb.get_classic_loadbalancer()


    ###########################################################################
    # Application Load Balancer
    ###########################################################################

    def test_list_application_load_balancer(self):
        lbs = elb.list_application_loadbalancer()
        lb_arn = cfm.get_resource_id(VPC_STACK, 'LoadBalancer')
        found = [ lb['LoadBalancerArn'] for lb in lbs if lb['LoadBalancerArn'] == lb_arn ]
        self.assertNotEqual(found, [])


    def test_get_application_load_balancer(self):
        lb_arn = cfm.get_resource_id(VPC_STACK, 'LoadBalancer')
        lb = elb.get_application_loadbalancer(arn=lb_arn)
        self.assertIsNotNone(lb)

        name = lb['LoadBalancerName']
        lb = elb.get_application_loadbalancer(name=name)
        self.assertIsNotNone(lb)

    
    def test_get_application_load_balancer_nonexistent(self):
        lb = elb.get_application_loadbalancer(arn='bogus')
        self.assertIsNone(lb)
        lb = elb.get_application_loadbalancer(name='garbage')
        self.assertIsNone(lb)


    def test_get_application_load_balancer_fail(self):
        with self.assertRaises(Exception):
            elb.get_application_loadbalancer()


    ###########################################################################
    # Target Groups
    ###########################################################################

    def test_list_target_groups(self):
        tgs = elb.list_target_groups()
        self.assertNotEqual(tgs, [])


    def test_get_target_group(self):
        tgid = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')
        tg = elb.get_target_group(arn=tgid)
        self.assertIsNotNone(tg)

        name = tg['TargetGroupName']
        tg = elb.get_target_group(name=name)
        self.assertIsNotNone(tg)


    def test_get_target_group_nonexistent(self):
        tg = elb.get_target_group(arn='bogus')
        self.assertIsNone(tg)
        tg = elb.get_target_group(name='garbage')
        self.assertIsNone(tg)


    def test_get_target_group_fail(self):
        with self.assertRaises(Exception):
            elb.get_target_group()


    def test_add_target(self):
        ec2.set_current_vpcid(VPC)
        group_arn = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')
        group_name = elb.get_target_group(arn=group_arn)['TargetGroupName']
        target_arn = cfm.get_resource_id(BASTION_STACK, 'Bastion')
        target = ec2.get_instance(instance_id=target_arn)
        target_name = ec2.get_tag_value(target, 'Name')

        result = elb.add_target(group_arn=group_arn, target_arn=target_arn, port=8080)
        self.assertTrue(result)
        region.get_elbv2().deregister_targets(TargetGroupArn=group_arn, Targets=[{'Id': target_arn}])

        result = elb.add_target(group_name=group_name, target_name=target_name)
        self.assertTrue(result, f'group_name={group_name}, target_name={target_name}')
        region.get_elbv2().deregister_targets(TargetGroupArn=group_arn, Targets=[{'Id': target_arn}])


    def test_add_target_nonexistent_instance(self):
        ec2.set_current_vpcid(VPC)
        tg_arn = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')

        result = elb.add_target(group_arn=tg_arn, target_arn='bogus')
        self.assertFalse(result)
        result = elb.add_target(group_arn=tg_arn, target_name='garbage')
        self.assertFalse(result)


    def test_add_target_nonexistent_target_group(self):
        ec2.set_current_vpcid(VPC)
        target_arn = cfm.get_resource_id(BASTION_STACK, 'Bastion')

        result = elb.add_target(group_arn='bogus', target_arn=target_arn)
        self.assertFalse(result)
        result = elb.add_target(group_name='garbage', target_arn=target_arn)
        self.assertFalse(result)


    def test_add_target_fail(self):
        tg_arn = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')
        target_arn = cfm.get_resource_id(BASTION_STACK, 'Bastion')

        result = elb.add_target(group_arn=tg_arn)
        self.assertFalse(result)
        result = elb.add_target(target_arn=target_arn)
        self.assertFalse(result)


    def test_get_targets_in_group(self):
        ec2.set_current_vpcid(VPC)
        group_arn = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')
        group_name = elb.get_target_group(arn=group_arn)['TargetGroupName']
        target_arn = cfm.get_resource_id(BASTION_STACK, 'Bastion')

        def find(target_id, results):
            match = ( result['Target']['Id'] for result in results if result['Target']['Id'] == target_id )
            return next(match, None)

        results = elb.get_targets_in_group(group_arn=group_arn)
        self.assertIsNotNone(find(target_arn, results))

        results = elb.get_targets_in_group(group_name=group_name)
        self.assertIsNotNone(find(target_arn, results))


    def test_get_targets_in_group_nonexistent(self):
        results = elb.get_targets_in_group(group_arn='bogus')
        self.assertFalse(results)
        results = elb.get_targets_in_group(group_name='garbage')
        self.assertFalse(results)


    def test_get_targets_in_group_fail(self):
        results = elb.get_targets_in_group()
        self.assertFalse(results)


    def test_get_elb_tags(self):
        tg_arn = cfm.get_resource_id(VPC_STACK, 'TargetGroup1')
        lb_arn = cfm.get_resource_id(VPC_STACK, 'LoadBalancer')
        tags = elb.get_elb_tags(tg_arn)
        self.assertNotEqual(tags, [])
        tags = elb.get_elb_tags(lb_arn)
        self.assertNotEqual(tags, [])


    def test_get_certs(self):
        certs = elb.get_certs()
        self.assertNotEqual(certs, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)