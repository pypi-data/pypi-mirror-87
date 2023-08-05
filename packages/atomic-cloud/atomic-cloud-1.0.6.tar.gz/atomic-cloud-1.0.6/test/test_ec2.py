import unittest
from aws import ec2, cluster, cfm, region
from test import test_cluster
import warnings
from os import path


VPC_NAME = test_cluster.CONFIG.vpc_name

HOSTED_ZONE_STACK = None
VPC_STACK = None
VPC = None
VPC_ID = None
KP = None


def _abs_path(file: str):
    basedir = path.abspath(path.dirname(__file__))
    return path.join(basedir, file)


class TestEC2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)

        global VPC_STACK, VPC, VPC_ID, KP, HOSTED_ZONE_STACK

        vpc = cluster.get_vpc(VPC_NAME)
        cp = cluster.get_cp(VPC_NAME)
        workers = cluster.get_eks_workers(VPC_NAME)
        if not vpc or not cp or not workers:
            raise RuntimeError('must call test_cluster.create_test_cluster() prior to this test')

        HOSTED_ZONE_STACK = cfm.create_stack(
            _abs_path('templates/hosted-zone.yaml'),
            stack_name='unit-hosted-zone',
            params={'VpcId': cfm.get_output(vpc, 'VPC')})
        
        VPC_STACK = vpc
        VPC_ID = cfm.get_output(VPC_STACK, 'VPC')
        VPC = region.get_ec2().describe_vpcs(Filters=[{'Name': 'vpc-id', 'Values': [VPC_ID]}]).get('Vpcs')[0]

        if ec2.key_pair_exists(VPC_NAME):
            region.get_ec2().delete_key_pair(KeyName=VPC_NAME)
        KP = region.get_ec2().create_key_pair(KeyName=VPC_NAME)


    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(HOSTED_ZONE_STACK['StackName'])
        region.get_ec2().delete_key_pair(KeyName=KP.get('KeyName'))


    def tearDown(self):
        ec2.set_current_vpcid(None)


    def test_list_regions(self):
        regions = ec2.list_regions()
        self.assertIsNotNone(regions)
        self.assertNotEqual(regions, [])
        self.assertIn('RegionName', regions[0])


    def test_list_azs(self):
        azs = ec2.list_azs()
        self.assertIsNotNone(azs)
        self.assertNotEqual(azs, [])
        self.assertIn('ZoneName', azs[0])


    ###########################################################################
    # VPC
    ###########################################################################

    def test_set_current_vpc(self):
        ec2.set_current_vpcid(vpcid=VPC_ID)
        current_vpcid = ec2.get_current_vpcid()
        self.assertEqual(current_vpcid, VPC_ID)

        ec2.set_current_vpcid(vpc=VPC)
        current_vpcid = ec2.get_current_vpcid()
        self.assertEqual(current_vpcid, VPC_ID)

        vpc_filter = ec2.get_vpc_filter()
        self.assertIsNotNone(vpc_filter)
        self.assertGreater(len(vpc_filter), 0)
        self.assertEqual(vpc_filter[0].get('Name'), 'vpc-id')
        self.assertIn(VPC_ID, vpc_filter[0].get('Values'))


    def test_get_current_vpc_fail(self):
        with self.assertRaises(Exception):
            ec2.get_current_vpcid()

    
    def test_get_vpc_filter_fail(self):
        with self.assertRaises(Exception):
            ec2.get_vpc_filter()


    def test_list_vpcs(self):
        vpcs = ec2.list_vpcs()
        self.assertIsNotNone(vpcs)
        self.assertGreater(len(vpcs), 0)


    def test_get_vpc(self):
        vpc = ec2.get_vpc(vpcid=VPC_ID)
        self.assertEqual(vpc, VPC)

        vpc = ec2.get_vpc(name=ec2.get_tag_value(VPC, 'Name'))
        self.assertEqual(vpc, VPC)


    def test_get_vpc_fail(self):
        with self.assertRaises(Exception):
            ec2.get_vpc()


    def test_get_vpcid(self):
        vpcid = ec2.get_vpcid(VPC)
        self.assertEqual(vpcid, VPC.get('VpcId'))


    ###########################################################################
    # Subnets
    ###########################################################################

    def test_list_subnets(self):
        ec2.set_current_vpcid(VPC)

        subnets = ec2.list_subnets()
        self.assertNotEqual(subnets, [])

        subnets = ec2.list_subnets(search_filter={'VpcName': VPC_NAME})
        self.assertNotEqual(subnets, [])

        subnets = ec2.list_subnets(subnet_type='garbage')
        self.assertEqual(subnets, [])

    
    def test_get_subnet(self):
        ec2.set_current_vpcid(VPC)
        existing_subnet = ec2.list_subnets()[0]

        existing_subnet_id = existing_subnet.get('SubnetId')
        found_subnet = ec2.get_subnet(existing_subnet_id)

        self.assertEqual(found_subnet, existing_subnet)


    def test_get_subnet_nonexistent(self):
        ec2.set_current_vpcid(VPC)
        bogus = ec2.get_subnet('garbage')
        self.assertIsNone(bogus)


    def test_get_subnet_id(self):
        ec2.set_current_vpcid(VPC)
        subnet = ec2.list_subnets()[0]
        self.assertEqual(ec2.get_subnet_id(subnet), subnet.get('SubnetId'))


    ###########################################################################
    # Internet Gateways & NATs
    ###########################################################################

    def test_list_igws(self):
        igws = ec2.list_igws()
        self.assertNotEqual(igws, [])


    def test_get_vpc_igw(self):
        ec2.set_current_vpcid(VPC)
        igw = ec2.get_vpc_igw()
        self.assertIsNotNone(igw)


    def test_list_nats(self):
        ec2.set_current_vpcid(VPC)
        nats = ec2.list_nats()
        self.assertNotEqual(nats, [])


    def test_list_eips(self):
        eips = ec2.list_eips()
        self.assertNotEqual(eips, [])


    ###########################################################################
    # Route Tables
    ###########################################################################

    def test_list_route_tables(self):
        ec2.set_current_vpcid(VPC)
        rts = ec2.list_route_tables()
        self.assertNotEqual(rts, [])
        rts = ec2.list_route_tables(search_filter={'VpcName': VPC_NAME})
        self.assertNotEqual(rts, [])


    def test_get_route_table(self):
        ec2.set_current_vpcid(VPC)
        public_rt_id = cfm.get_output(VPC_STACK, 'PublicRouteTable')

        public_rt = ec2.get_route_table(rt_id=public_rt_id)
        self.assertIsNotNone(public_rt)

        public_rt_name = ec2.get_tag_value(public_rt, 'Name')
        public_rt = ec2.get_route_table(name=public_rt_name)
        self.assertIsNotNone(public_rt)

        subnet_id = public_rt.get('Associations')[0].get('SubnetId')
        public_rt = ec2.get_route_table(subnet_id=subnet_id)
        self.assertIsNotNone(public_rt)


    def test_get_route_table_nonexistent(self):
        ec2.set_current_vpcid(VPC)
        found = ec2.get_route_table(name='phony')
        self.assertIsNone(found)
        found = ec2.get_route_table(rt_id='bogus')
        self.assertIsNone(found)
        found = ec2.get_route_table(subnet_id='garbage')
        self.assertIsNone(found)


    def test_get_route_table_fail(self):
        with self.assertRaises(Exception):
            ec2.get_route_table()


    def test_get_route_table_id(self):
        ec2.set_current_vpcid(VPC)
        rts = ec2.list_route_tables()
        rt = rts[0]
        rt_id = rt.get('RouteTableId')
        self.assertEqual(ec2.get_route_table_id(rt), rt_id)


    ###########################################################################
    # Security Groups
    ###########################################################################

    def test_list_sgs(self):
        ec2.set_current_vpcid(VPC)
        sgs = ec2.list_sgs()
        self.assertNotEqual(sgs, [])

        sgs = ec2.list_sgs(search_filter={'VpcName': VPC_NAME})
        self.assertNotEqual(sgs, [])


    def test_get_sg(self):
        ec2.set_current_vpcid(VPC)
        sgs = ec2.list_sgs()
        sg = sgs[0]
        sgid = sg.get('GroupId')
        self.assertEqual(ec2.get_sg(sgid=sgid), sg)

        sg_name = ec2.get_tag_value(sg, 'Name')
        self.assertEqual(ec2.get_sg(name=sg_name), sg)


    def test_get_sg_fail(self):
        with self.assertRaises(Exception):
            ec2.get_sg()


    def test_get_sg_nonexistent(self):
        ec2.set_current_vpcid(VPC)
        found = ec2.get_sg(name='bogus')
        self.assertIsNone(found)
        found = ec2.get_sg(sgid='garbage')
        self.assertIsNone(found)


    def test_get_sgid(self):
        ec2.set_current_vpcid(VPC)
        sgs = ec2.list_sgs()
        sg = sgs[0]
        sgid = sg.get('GroupId')
        self.assertEqual(ec2.get_sgid(sg), sgid)


    ###########################################################################
    # KeyPairs
    ###########################################################################

    def test_create_key_pair(self):
        try:
            kp = ec2.create_key_pair('key_pair')
            self.assertIsNotNone(kp)

            same_kp = ec2.create_key_pair('key_pair')
            self.assertIsNone(same_kp)
        finally:
            region.get_ec2().delete_key_pair(KeyName='key_pair')

    
    def test_list_key_pairs(self):
        found_kps = ec2.list_key_pairs()
        self.assertNotEqual(found_kps, [])
        found_kps = ec2.list_key_pairs(name=KP.get('KeyName'))
        self.assertNotEqual(found_kps, [])
        self.assertEqual(found_kps[0].get('KeyFingerprint'), KP.get('KeyFingerprint'))


    def test_key_pair_exists(self):
        self.assertTrue(ec2.key_pair_exists(name=KP.get('KeyName')))


    def test_delete_key_pair(self):
        kp_name = 'test-delete'
        region.get_ec2().create_key_pair(KeyName=kp_name)

        ec2.delete_key_pair(name=kp_name)

        found_kps = ec2.list_key_pairs(name=kp_name)
        self.assertEqual(found_kps, [])


    def test_delete_key_pair_nonexistent(self):
        result = ec2.delete_key_pair('bogus')
        self.assertIsNone(result)


    def test_wait_for_key_pair(self):
        try:
            kp_name = 'test-wait'

            exists = ec2.wait_for_key_pair(name=kp_name, interval = 1, timeout=2)
            self.assertFalse(exists)

            region.get_ec2().create_key_pair(KeyName=kp_name)

            exists = ec2.wait_for_key_pair(name=kp_name)
            self.assertTrue(exists)
        finally:
            region.get_ec2().delete_key_pair(KeyName=kp_name)


    ###########################################################################
    # AMIs
    ###########################################################################

    def test_get_linux2_ami(self):
        ami = ec2.get_linux2_ami()
        self.assertIsNotNone(ami)


    def test_get_image(self):
        imageid = ec2.get_linux2_ami()
        image = ec2.get_image(imageid)
        self.assertIsNotNone(image)


    ###########################################################################
    # EC2 Instances
    ###########################################################################

    def test_list_instances(self):
        ec2.set_current_vpcid(VPC)
        instances = ec2.list_instances()
        self.assertNotEqual(instances, [])

        instance = instances[0]
        tags = { tag.get('Key') : tag.get('Value') for tag in instance.get('Tags') }
        filtered_instances = ec2.list_instances(search_filter=tags)
        self.assertIn(instance, filtered_instances)


    def test_get_instance(self):
        ec2.set_current_vpcid(VPC)
        instance = ec2.list_instances()[0]

        instance_id = instance.get('InstanceId')
        found_instance = ec2.get_instance(instance_id=instance_id)
        self.assertEqual(found_instance, instance)


    def test_get_instance_fail(self):
        with self.assertRaises(Exception):
            ec2.get_instance()


    def test_get_instance_id(self):
        ec2.set_current_vpcid(VPC)
        instance = ec2.list_instances()[0]
        instance_id = instance.get('InstanceId')
        self.assertEqual(ec2.get_instance_id(instance), instance_id)


    ###########################################################################
    # Tags
    ###########################################################################

    def test_get_tag_value(self):
        value = ec2.get_tag_value(VPC, 'Name')
        self.assertIsNotNone(value)

    
    def test_get_tag_value_nonexistent(self): 
        value = ec2.get_tag_value(VPC, 'bogus')
        self.assertIsNone(value)


    def test_get_ec2_tags(self):
        ec2.set_current_vpcid(VPC)
        instance = ec2.list_instances()[0]
        instance_id = ec2.get_instance_id(instance)

        tags_from_obj = ec2.get_ec2_tags(aws_obj=instance)
        tags_from_instance_id = ec2.get_ec2_tags(instance_id=instance_id)
        
        for tag_pair in instance.get('Tags'):
            key = tag_pair.get('Key')
            value = tag_pair.get('Value')
            self.assertEqual(tags_from_obj.get(key), value)
            self.assertEqual(tags_from_instance_id.get(key), value)


    def test_match_tags(self):
        tags = ec2.get_ec2_tags(VPC_STACK)
        match = ec2.match_tags(tags, VPC_STACK)
        self.assertTrue(match)


    def test_set_tag(self):
        ec2.set_current_vpcid(VPC)
        instance_id = ec2.list_instances()[0].get('InstanceId')
        ec2.set_tag('Hello', 'World', instance_id=instance_id)
        instance = ec2.get_instance(instance_id=instance_id)
        self.assertTrue(ec2.match_tags({'Hello': 'World'}, instance))


    def test_set_tag_fail(self):
        self.assertIsNone(ec2.set_tag('key', 'value'))
        

    def test_wait_for_ready(self):
        ec2.set_current_vpcid(VPC)

        instance = ec2.list_instances()[0]
        instance_id = instance.get('InstanceId')

        ready = ec2.wait_for_ready(instance_id=instance_id, interval=1, timeout=1)
        self.assertFalse(ready)

        ec2.set_tag('Ready', 'True', instance_id=instance_id)

        ready = ec2.wait_for_ready(instance_id=instance_id, interval=1, timeout=10)
        self.assertTrue(ready)

        ec2.set_tag('Ready', 'False', instance_id=instance_id)


    def test_wait_for_ready_nonexistent(self):
        ec2.set_current_vpcid(VPC)
        result = ec2.wait_for_ready(name='bogus', instance_id='garbage')
        self.assertIsNone(result)


    def test_wait_for_ready_fail(self):
        self.assertIsNone(ec2.wait_for_ready())


    ###########################################################################
    # SSM
    ###########################################################################

    def test_ssm_run_shell_script(self):
        ec2.set_current_vpcid(ec2.get_vpc(default=True))
        try:
            cfm.create_stack(_abs_path('templates/unit-basic-ssm.yaml'), stack_name='unit-run-shell-script', capabilities=['CAPABILITY_NAMED_IAM'])
            ec2.wait_for_ready(name = 'unit-test-ssm-instance', timeout = 240)
            commands = ['echo hello', 'echo world']
            response = ec2.ssm_run_shell_script(name = 'unit-test-ssm-instance', commands = commands, comment = 'test run shell script')
            self.assertIsNotNone(response)
            self.assertEqual('test run shell script', response['Command']['Comment'])
        finally:
            cfm.delete_stack('unit-run-shell-script')


    ###########################################################################
    # Route53
    ###########################################################################

    def test_list_hosted_zones(self):
        expected_zones = region.get_route53().list_hosted_zones().get('HostedZones', [])
        returned_zones = ec2.list_hosted_zones()
        self.assertNotEqual(returned_zones, [])
        self.assertEqual(returned_zones, expected_zones)


    def test_get_zone_vpc_ids(self):
        zone_id = cfm.get_output(HOSTED_ZONE_STACK, 'HostedZone')
        vpc_ids = ec2.get_zone_vpc_ids(zone_id)
        self.assertIn(VPC_ID, vpc_ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)