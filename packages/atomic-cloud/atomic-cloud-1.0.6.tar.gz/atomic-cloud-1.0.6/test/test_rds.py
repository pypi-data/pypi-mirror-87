import unittest
import warnings
from os import path
from aws import rds, cluster, cfm
from test import test_cluster


VPC_NAME = test_cluster.CONFIG.vpc_name

DB_CLUSTER_ID = None
DB_CLUSTER_ENGINE = None
DB_INSTANCE_ID = None
DB_INSTANCE_ENGINE = None
DB_SG = None


def _abs_path(file: str):
    basedir = path.abspath(path.dirname(__file__))
    return path.join(basedir, file)


class TestRDS(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Hide boto3 warnings. This is a known issue with boto3 + unittest.
        warnings.simplefilter('ignore', category=ResourceWarning)
        
        rds_stack = cluster.get_rds(VPC_NAME)
        if not rds_stack:
            raise RuntimeError('must call test_cluster.create_test_cluster() prior to this test')

        db_cluster_stack = cfm.create_stack(
            _abs_path('templates/rds-db-cluster.yaml'),
            stack_name=f'{VPC_NAME}-db-cluster',
            params={'EnvType': VPC_NAME})

        global DB_CLUSTER_ID, DB_CLUSTER_ENGINE, DB_INSTANCE_ID, DB_INSTANCE_ENGINE, DB_SG
        DB_CLUSTER_ID = cfm.get_output(db_cluster_stack, 'DBCluster')
        DB_CLUSTER_ENGINE = rds.get_db_cluster(DB_CLUSTER_ID)['Engine']
        DB_INSTANCE_ID = cfm.get_output(rds_stack, 'DBInstance')
        DB_INSTANCE_ENGINE = rds.get_db_instance(DB_INSTANCE_ID)['Engine']
        DB_SG = cfm.get_output(rds_stack, 'DBSecurityGroup')


    @classmethod
    def tearDownClass(cls):
        cfm.delete_stack(f'{VPC_NAME}-db-cluster')


    ###########################################################################
    # Database Clusters
    ###########################################################################
    
    def test_list_db_clusters(self):
        all_clusters = rds.list_db_clusters()
        self.assertNotEqual(all_clusters, [])

        filtered_clusters = rds.list_db_clusters(engine=DB_CLUSTER_ENGINE)
        self.assertNotEqual(filtered_clusters, [])


    def test_list_db_clusters_nonexistent_engine(self):
        with self.assertRaises(Exception):
            rds.list_db_clusters(engine='bogus')


    def test_get_db_cluster(self):
        result = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertIsNotNone(result)


    def test_get_db_cluster_nonexistent(self):
        result = rds.get_db_cluster('bogus')
        self.assertIsNone(result)


    def test_set_cluster_delete_protection(self):
        rds.set_db_cluster_delete_protection(DB_CLUSTER_ID, protect=True)
        db_cluster = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertTrue(db_cluster['DeletionProtection'])

        rds.set_db_cluster_delete_protection(DB_CLUSTER_ID, protect=False)
        db_cluster = rds.get_db_cluster(DB_CLUSTER_ID)
        self.assertFalse(db_cluster['DeletionProtection'])

    
    ###########################################################################
    # Database Instances
    ###########################################################################

    def test_list_db_instances(self):
        all_instances = rds.list_db_instances()
        self.assertNotEqual(all_instances, [])

        filtered_by_engine = rds.list_db_instances(engine=DB_INSTANCE_ENGINE)
        self.assertNotEqual(filtered_by_engine, [])

        filtered_by_cluster = rds.list_db_instances(cluster_id=DB_CLUSTER_ID)
        self.assertEqual(filtered_by_cluster, [])


    def test_get_db_instance(self):
        result = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertIsNotNone(result)


    def test_get_db_instance_nonexistent(self):
        result = rds.get_db_instance('bogus')
        self.assertIsNone(result)


    def test_set_db_instance_delete_protection(self):
        rds.set_db_instance_delete_protection(DB_INSTANCE_ID, protect=True)
        db_instance = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertTrue(db_instance['DeletionProtection'])

        rds.set_db_instance_delete_protection(DB_INSTANCE_ID, protect=False)
        db_instance = rds.get_db_instance(DB_INSTANCE_ID)
        self.assertFalse(db_instance['DeletionProtection'])


    ###########################################################################
    # Database Subnet Groups
    ###########################################################################

    def test_list_subnet_groups(self):
        groups = rds.list_subnet_groups()
        self.assertNotEqual(groups, [])


    def test_get_subnet_group(self):
        subnet_group_name = rds.get_db_instance(DB_INSTANCE_ID)['DBSubnetGroup']['DBSubnetGroupName']
        subnet_group = rds.get_subnet_group(subnet_group_name)
        self.assertIsNotNone(subnet_group)

    
    def test_get_subnet_group_nonexistent(self):
        subnet_group = rds.get_subnet_group('bogus')
        self.assertIsNone(subnet_group)


    ###########################################################################
    # Database Security Groups
    ###########################################################################

    def test_list_db_sgs(self):
        sgs = rds.list_db_sgs()
        self.assertNotEqual(sgs, [])


    def test_get_db_sg(self):
        sg_name = rds.list_db_sgs()[0]['DBSecurityGroupName']
        found_sg = rds.get_db_sg(sg_name)
        self.assertEqual(found_sg['DBSecurityGroupName'], sg_name)


    def test_get_db_sg_nonexistent(self):
        found = rds.get_db_sg('bogus')
        self.assertIsNone(found)


    ###########################################################################
    # Tags
    ###########################################################################

    def test_get_rds_tags(self):
        arn = rds.get_db_instance(DB_INSTANCE_ID)['DBInstanceArn']
        tags = rds.get_rds_tags(arn)
        self.assertNotEqual(tags, {})
    

if __name__ == "__main__":
    unittest.main()