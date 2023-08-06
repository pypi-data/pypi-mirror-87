import boto3
from aws.region import get_rds

###########################################################################
# Database Clusters & Instances
###########################################################################

def list_db_clusters(engine: dict = None):
    """
    List of all database clusters in the environment

    :param engine: Optional engine type of the database cluster
    :return: `Database Cluster Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_clusters>`_

    Example Output::

        [
            {
                AllocatedStorage: 1
                AvailabilityZones: [
                    "us-east-1c"
                    "us-east-1b"
                    "us-east-1a"
                ]
                BackupRetentionPeriod: 1
                DatabaseName: ""
                DBClusterIdentifier: "database-1"
                DBClusterParameterGroup: "default.aurora5.6"
                DBSubnetGroup: "default-vpc-098ec64bb7f6e4799"
                Status: "available"
                EarliestRestorableTime: 2019-11-13 10:37:42.998000+00:00
                Endpoint: "database-1.cluster-cliglprpku2i.us-east-1.rds.amazonaws.com"
                ReaderEndpoint: "database-1.cluster-ro-cliglprpku2i.us-east-1.rds.amazonaws.com"
                MultiAZ: False
                Engine: "aurora"
                EngineVersion: "5.6.10a"
                LatestRestorableTime: 2019-11-14 20:39:01.484000+00:00
                Port: 3306
                MasterUsername: "admin"
                PreferredBackupWindow: "10:25-10:55"
                PreferredMaintenanceWindow: "mon:06:39-mon:07:09"
                ReadReplicaIdentifiers: []
                DBClusterMembers: [
                    {
                        DBInstanceIdentifier: "database-1-instance-1"
                        IsClusterWriter: True
                        DBClusterParameterGroupStatus: "pending-reboot"
                        PromotionTier: 1
                    }
                ]
                VpcSecurityGroups: [
                    {
                        VpcSecurityGroupId: "sg-0864e77f268788dd5"
                        Status: "active"
                    }
                ]
                HostedZoneId: "Z2R2ITUGPM61AM"
                StorageEncrypted: True
                KmsKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                DbClusterResourceId: "cluster-OQ3NVZTFVRMSNVJWY6K6FNHXWE"
                DBClusterArn: "arn:aws:rds:us-east-1:683863474030:cluster:database-1"
                AssociatedRoles: []
                IAMDatabaseAuthenticationEnabled: False
                ClusterCreateTime: 2019-11-08 19:38:29.519000+00:00
                EngineMode: "provisioned"
                DeletionProtection: False
                HttpEndpointEnabled: False
                ActivityStreamStatus: "stopped"
                CopyTagsToSnapshot: True
                CrossAccountClone: False
            }
        ]

    """

    if engine is not None:
        clusterList = get_rds().describe_db_clusters(Filters=[{'Name': 'engine','Values': [engine]}]).get('DBClusters')
    else:
        clusterList = get_rds().describe_db_clusters().get('DBClusters')

    return clusterList

def get_db_cluster(id: str):
    """
    Get details of a specific database cluster

    :param id: The name of the database cluster
    :return: `Database Cluster Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_clusters>`_

    """

    clusters = get_rds().describe_db_clusters(Filters=[{'Name': 'db-cluster-id','Values': [id]}]).get('DBClusters')
    return clusters[0] if clusters else None

def set_db_cluster_delete_protection(id: str, protect: bool):
    """
    Set the delete protection configuration of the specified database cluster

    :param id: The name of the database cluster
    :param protect: If true, delete protection is enabled for the database cluster.
    :return: N/A

    """

    get_rds().modify_db_cluster(DBClusterIdentifier=id,DeletionProtection=protect)

def list_db_instances(cluster_id: str = None, engine: str = None):
    """
    List all the database instances in the environment

    :param cluster_id: Optional name of the database cluster
    :param engine: Optional engine of the database instance
    :return: `Database Instance Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances>`_

    Example Output::

        [
            {
                DBInstanceIdentifier: "database-1-instance-1"
                DBInstanceClass: "db.r5.large"
                Engine: "aurora"
                DBInstanceStatus: "available"
                MasterUsername: "admin"
                Endpoint: {
                    Address: "database-1-instance-1.cliglprpku2i.us-east-1.rds.amazonaws.com"
                    Port: 3306
                    HostedZoneId: "Z2R2ITUGPM61AM"
                }
                AllocatedStorage: 1
                InstanceCreateTime: 2019-11-08 19:42:38.941000+00:00
                PreferredBackupWindow: "10:25-10:55"
                BackupRetentionPeriod: 1
                DBSecurityGroups: []
                VpcSecurityGroups: [
                    {
                        VpcSecurityGroupId: "sg-0864e77f268788dd5"
                        Status: "active"
                    }
                ]
                DBParameterGroups: [
                    {
                        DBParameterGroupName: "default.aurora5.6"
                        ParameterApplyStatus: "in-sync"
                    }
                ]
                AvailabilityZone: "us-east-1b"
                DBSubnetGroup: {
                    DBSubnetGroupName: "default-vpc-098ec64bb7f6e4799"
                    DBSubnetGroupDescription: "Created from the RDS Management Console"
                    VpcId: "vpc-098ec64bb7f6e4799"
                    SubnetGroupStatus: "Complete"
                    Subnets: [
                        {
                            SubnetIdentifier: "subnet-01777641646dce71d"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1b"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-022e237798060f8de"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1b"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-096fe6360d7096d4f"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1c"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-0a0ededb6d5cec867"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1c"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-0ed958b196df664ac"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1a"
                            }
                            SubnetStatus: "Active"
                        }
                        {
                            SubnetIdentifier: "subnet-01482395eb32b7e33"
                            SubnetAvailabilityZone: {
                                Name: "us-east-1a"
                            }
                            SubnetStatus: "Active"
                        }
                    ]
                }
                PreferredMaintenanceWindow: "sat:04:17-sat:04:47"
                PendingModifiedValues: {}
                MultiAZ: False
                EngineVersion: "5.6.10a"
                AutoMinorVersionUpgrade: True
                ReadReplicaDBInstanceIdentifiers: []
                LicenseModel: "general-public-license"
                OptionGroupMemberships: [
                    {
                        OptionGroupName: "default:aurora-5-6"
                        Status: "in-sync"
                    }
                ]
                PubliclyAccessible: False
                StorageType: "aurora"
                DbInstancePort: 0
                DBClusterIdentifier: "database-1"
                StorageEncrypted: True
                KmsKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                DbiResourceId: "db-FDGE6FEF2D45HYI4N4TT4KBFRU"
                CACertificateIdentifier: "rds-ca-2015"
                DomainMemberships: []
                CopyTagsToSnapshot: False
                MonitoringInterval: 60
                EnhancedMonitoringResourceArn: "arn:aws:logs:us-east-1:683863474030:log-group:RDSOSMetrics:log-stream:db-FDGE6FEF2D45HYI4N4TT4KBFRU"
                MonitoringRoleArn: "arn:aws:iam::683863474030:role/rds-monitoring-role"
                PromotionTier: 1
                DBInstanceArn: "arn:aws:rds:us-east-1:683863474030:db:database-1-instance-1"
                IAMDatabaseAuthenticationEnabled: False
                PerformanceInsightsEnabled: True
                PerformanceInsightsKMSKeyId: "arn:aws:kms:us-east-1:683863474030:key/c7c7bfb8-3225-4da1-8724-9e06ddf0cff6"
                PerformanceInsightsRetentionPeriod: 7
                DeletionProtection: False
                AssociatedRoles: []
            }
        ]

    """

    if cluster_id is not None:
        instanceList = get_rds().describe_db_instances(Filters=[{'Name': 'db-cluster-id','Values': [cluster_id]}]).get('DBInstances')
    elif engine is not None:
        instanceList = get_rds().describe_db_instances(Filters=[{'Name': 'engine','Values': [engine]}]).get('DBInstances')
    else:
        instanceList = get_rds().describe_db_instances().get('DBInstances')
    return instanceList

def get_db_instance(id: str):
    """
    Get details of a specific database instance

    :param id: The name of the database instance
    :return: `Database Instance Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances>`_

    """

    instances = get_rds().describe_db_instances(Filters=[{'Name': 'db-instance-id','Values': [id]}]).get('DBInstances')
    return instances[0] if instances else None

def set_db_instance_delete_protection(id: str, protect: bool):
    """
    Set the delete protection configuration of the specified database instance

    :param id: The name of the database instance
    :param protect: If true, delete protection is enabled for the database instance.
    :return: N/A

    """
    get_rds().modify_db_instance(DBInstanceIdentifier=id,DeletionProtection=protect)

###########################################################################
# Database Subnet Groups
###########################################################################

def list_subnet_groups():
    """
    List all database subnet groups

    :return: `Database Subnet Groups Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_subnet_groups>`_

    Example Output::

        [
            {
                DBSubnetGroupName: "default"
                DBSubnetGroupDescription: "default"
                VpcId: "vpc-c74fccbd"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-683f4246"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-fe9ab3f1"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1f"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-42c8b81e"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-5045431a"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1d"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-86d16bb8"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1e"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-1dec9b7a"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:default"
            }
            {
                DBSubnetGroupName: "default-vpc-098ec64bb7f6e4799"
                DBSubnetGroupDescription: "Created from the RDS Management Console"
                VpcId: "vpc-098ec64bb7f6e4799"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-01777641646dce71d"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-022e237798060f8de"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-096fe6360d7096d4f"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0a0ededb6d5cec867"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1c"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0ed958b196df664ac"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-01482395eb32b7e33"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:default-vpc-098ec64bb7f6e4799"
            }
            {
                DBSubnetGroupName: "test"
                DBSubnetGroupDescription: "test subnet group"
                VpcId: "vpc-098ec64bb7f6e4799"
                SubnetGroupStatus: "Complete"
                Subnets: [
                    {
                        SubnetIdentifier: "subnet-01777641646dce71d"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1b"
                        }
                        SubnetStatus: "Active"
                    }
                    {
                        SubnetIdentifier: "subnet-0ed958b196df664ac"
                        SubnetAvailabilityZone: {
                            Name: "us-east-1a"
                        }
                        SubnetStatus: "Active"
                    }
                ]
                DBSubnetGroupArn: "arn:aws:rds:us-east-1:683863474030:subgrp:test"
            }
        ]

    """
    db_subnet_groups = get_rds().describe_db_subnet_groups().get('DBSubnetGroups')
    return db_subnet_groups

def get_subnet_group(id: str):
    """
    Get details of a specific subnet group

    :param id: The name of the subnet group
    :return: `Database Subnet Groups Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_subnet_groups>`_

    """
    for group in list_subnet_groups():
        if group['DBSubnetGroupName'] == id:
            return group
    return None


###########################################################################
# Database Security Groups
###########################################################################
def list_db_sgs():
    """
    List all database security groups

    :return: `Database Security Groups Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_security_groups>`_

    Example Output::

        [
            {
                OwnerId: "683863474030"
                DBSecurityGroupName: "default"
                DBSecurityGroupDescription: "default"
                EC2SecurityGroups: []
                IPRanges: []
                DBSecurityGroupArn: "arn:aws:rds:us-east-1:683863474030:secgrp:default"
            }
        ]

    """

    db_security_groups = get_rds().describe_db_security_groups().get('DBSecurityGroups')
    return db_security_groups

def get_db_sg(id: str):
    """
    List the details of a specific database security group

    :param id: The name of the database security group
    :return: `Database Security Groups Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_security_groups>`_

    """
    for group in list_db_sgs():
        if group['DBSecurityGroupName'] == id:
            return group
    return None

###########################################################################
# Tags
###########################################################################
def get_rds_tags(arn: str):
    """
    List the tags associated with the RDS object

    :param obj: The ARN of the object or the object in dictionary form to query for Tag element
    :return: The tags associated with the RDS object

    ExampleOutput::

        {
            Env: "test"
            Name: "database-1-instance-1"
        }

    """
    tagList = get_rds().list_tags_for_resource(ResourceName=arn).get("TagList")
    res = {}
    for x in tagList:
        key = x.get('Key')
        val = x.get('Value')
        res[key] = val
    return res