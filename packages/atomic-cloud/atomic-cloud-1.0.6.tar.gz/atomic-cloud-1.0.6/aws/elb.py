import boto3
import ast
from aws.ec2 import get_instance, set_current_vpcid, get_vpc
from aws.region import get_elb, get_elbv2, get_acm

###########################################################################
# Elastic Load Balancers
###########################################################################

def list_classic_loadbalancer():
    """
    List all the load balancers.

    :return: `Load Balancer Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers>`_

    Example Output::

        [
            {
                'LoadBalancerName': 'afe5ad6b1ef9211e989160e055464502',
                'DNSName': 'afe5ad6b1ef9211e989160e055464502-1139835294.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneName': 'afe5ad6b1ef9211e989160e055464502-1139835294.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneNameID': 'Z35SXDOTRQ7X7K',
                'ListenerDescriptions': [
                    {
                        'Listener': {
                            'Protocol': 'TCP',
                            'LoadBalancerPort': 80,
                            'InstanceProtocol': 'TCP',
                            'InstancePort': 32540
                        },
                        'PolicyNames': [
                        ]
                    },
                    {
                        'Listener': {
                            'Protocol': 'TCP',
                            'LoadBalancerPort': 443,
                            'InstanceProtocol': 'TCP',
                            'InstancePort': 30054
                        },
                        'PolicyNames': [
                        ]
                    }
                ],
                'Policies': {
                    'AppCookieStickinessPolicies': [
                    ],
                    'LBCookieStickinessPolicies': [
                    ],
                    'OtherPolicies': [
                    ]
                },
                'BackendServerDescriptions': [
                ],
                'AvailabilityZones': [
                    'us-east-1a'
                ],
                'Subnets': [
                    'subnet-0ed958b196df664ac'
                ],
                'VPCId': 'vpc-098ec64bb7f6e4799',
                'Instances': [
                    {
                        'InstanceId': 'i-04154257c34275a66'
                    },
                    {
                        'InstanceId': 'i-05a62b08d2a054fcc'
                    },
                    {
                        'InstanceId': 'i-0a077d24bb15a57d4'
                    }
                ],
                'HealthCheck': {
                    'Target': 'TCP:32540',
                    'Interval': 10,
                    'Timeout': 5,
                    'UnhealthyThreshold': 6,
                    'HealthyThreshold': 2
                },
                'SourceSecurityGroup': {
                    'OwnerAlias': '683863474030',
                    'GroupName': 'k8s-elb-afe5ad6b1ef9211e989160e055464502'},
                    'SecurityGroups': [
                        'sg-0e717fd4674946864'
                        ],
                    'CreatedTime': datetime.datetime(2019, 10, 15, 21, 30, 30, 270000, tzinfo=tzutc()),
                    'Scheme': 'internet-facing'
                }
            },
            {
                'LoadBalancerName': 'a5e5fe8f4001511ea89160e055464502',
                    'DNSName': 'a5e5fe8f4001511ea89160e055464502-79608721.us-east-1.elb.amazonaws.com',
                    'CanonicalHostedZoneName': 'a5e5fe8f4001511ea89160e055464502-79608721.us-east-1.elb.amazonaws.com',
                    'CanonicalHostedZoneNameID': 'Z35SXDOTRQ7X7K',
                    'ListenerDescriptions': [
                        {
                            'Listener': {
                                'Protocol': 'TCP',
                                'LoadBalancerPort': 8080,
                                'InstanceProtocol': 'TCP',
                                'InstancePort': 30826
                            },
                            'PolicyNames': [
                            ]
                        }
                    ],
                    'Policies': {
                        'AppCookieStickinessPolicies': [
                        ],
                        'LBCookieStickinessPolicies': [
                        ],
                        'OtherPolicies': [
                        ]
                    },
                    'BackendServerDescriptions': [
                    ],
                    'AvailabilityZones': [
                        'us-east-1a'
                    ],
                    'Subnets': [
                        'subnet-0ed958b196df664ac'
                    ],
                    'VPCId': 'vpc-098ec64bb7f6e4799',
                    'Instances': [
                        {
                            'InstanceId': 'i-04154257c34275a66'
                        },
                        {
                            'InstanceId': 'i-05a62b08d2a054fcc'
                        },
                        {
                            'InstanceId': 'i-0a077d24bb15a57d4'
                        }
                    ],
                    'HealthCheck': {
                        'Target': 'TCP:30826',
                        'Interval': 10,
                        'Timeout': 5,
                        'UnhealthyThreshold': 6,
                        'HealthyThreshold': 2
                    },
                    'SourceSecurityGroup': {
                        'OwnerAlias': '683863474030',
                        'GroupName': 'k8s-elb-a5e5fe8f4001511ea89160e055464502'
                    },
                    'SecurityGroups': [
                        'sg-0be4b1290df50d44c'
                    ],
                    'CreatedTime': datetime.datetime(2019, 11, 5, 21, 43, 57, 650000, tzinfo=tzutc()),
                    'Scheme': 'internet-facing'
            }
        ]

    """
    elbList = get_elb().describe_load_balancers().get('LoadBalancerDescriptions')
    return elbList


def get_classic_loadbalancer(name: str = None):
    """
    List a specific load balancer. The load balancer's name must be provided for the search

    :param name: The name of the load balancer
    :return: `Load Balancer Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers>`_

    Example Output::

        [
            {
                'LoadBalancerName': 'a5e5fe8f4001511ea89160e055464502',
                'DNSName': 'a5e5fe8f4001511ea89160e055464502-79608721.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneName': 'a5e5fe8f4001511ea89160e055464502-79608721.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneNameID': 'Z35SXDOTRQ7X7K',
                'ListenerDescriptions': [
                    {
                        'Listener': {
                            'Protocol': 'TCP',
                            'LoadBalancerPort': 8080,
                            'InstanceProtocol': 'TCP',
                            'InstancePort': 30826
                        },
                        'PolicyNames': [
                        ]
                    }
                ],
                'Policies': {
                    'AppCookieStickinessPolicies': [
                    ],
                    'LBCookieStickinessPolicies': [
                    ],
                    'OtherPolicies': [
                    ]
                },
                'BackendServerDescriptions': [
                ],
                'AvailabilityZones': [
                    'us-east-1a'
                ],
                'Subnets': [
                    'subnet-0ed958b196df664ac'
                ],
                'VPCId': 'vpc-098ec64bb7f6e4799',
                'Instances': [
                    {
                        'InstanceId': 'i-04154257c34275a66'
                    },
                    {
                        'InstanceId': 'i-05a62b08d2a054fcc'
                    },
                    {
                        'InstanceId': 'i-0a077d24bb15a57d4'
                    }
                ],
                'HealthCheck': {
                    'Target': 'TCP:30826',
                    'Interval': 10,
                    'Timeout': 5,
                    'UnhealthyThreshold': 6,
                    'HealthyThreshold': 2
                },
                'SourceSecurityGroup': {
                    'OwnerAlias': '683863474030',
                    'GroupName': 'k8s-elb-a5e5fe8f4001511ea89160e055464502'
                },
                'SecurityGroups': [
                    'sg-0be4b1290df50d44c'
                ],
                'CreatedTime': datetime.datetime(2019, 11, 5, 21, 43, 57, 650000, tzinfo=tzutc()),
                'Scheme': 'internet-facing'
            }
        ]

    """
    elbList = list_classic_loadbalancer()
    if name is not None:
        for elb in elbList:
            if elb.get('LoadBalancerName') == name:
                return elb
    else:
        raise Exception('name must be provided for the search')
    return None


###########################################################################
# Elastic Load Balancers, Version 2
###########################################################################

def list_application_loadbalancer():
    """
    List all the application load balancers

    :return: `Application Load Balancer Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers>`_

    Example Output::

        [
            {
                'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:loadbalancer/app/np-load-balancer/ccad1344d28899a7',
                'DNSName': 'np-load-balancer-282693614.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneId': 'Z35SXDOTRQ7X7K',
                'CreatedTime': datetime.datetime(2019, 10, 15, 20, 6, 42, 440000, tzinfo=tzutc()),
                'LoadBalancerName': 'np-load-balancer', 'Scheme': 'internet-facing',
                'VpcId': 'vpc-098ec64bb7f6e4799',
                'State': {
                    'Code': 'active'
                },
                'Type': 'application',
                'AvailabilityZones': [
                    {
                        'ZoneName': 'us-east-1b',
                        'SubnetId': 'subnet-022e237798060f8de',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1c',
                        'SubnetId': 'subnet-0a0ededb6d5cec867',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1a',
                        'SubnetId': 'subnet-0ed958b196df664ac',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    }
                ],
                'SecurityGroups': [
                    'sg-0ec1f9503c4bc5d9b'
                ],
                'IpAddressType': 'ipv4'
            },
            {
                'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:loadbalancer/app/co-load-balancer/a30dcac13bc79379',
                'DNSName': 'co-load-balancer-847844731.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneId': 'Z35SXDOTRQ7X7K',
                'CreatedTime': datetime.datetime(2019, 10, 18, 13, 18, 10, 760000, tzinfo=tzutc()),
                'LoadBalancerName': 'co-load-balancer',
                'Scheme': 'internet-facing',
                'VpcId': 'vpc-07ad4bebf61a73a1b',
                'State': {
                    'Code': 'active'
                },
                'Type': 'application',
                'AvailabilityZones': [
                    {
                        'ZoneName': 'us-east-1a',
                        'SubnetId': 'subnet-0288ac3d52fdb275b',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1b',
                        'SubnetId': 'subnet-073e64e882c3163db',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1c',
                        'SubnetId': 'subnet-0f730fa7e355fea27',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    }
                ],
                'SecurityGroups': [
                    'sg-0da239213120f2a1a'
                ],
                'IpAddressType': 'ipv4'
            },
            {
                'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:loadbalancer/app/master-target/ace3895f0ceffca5',
                'DNSName': 'internal-master-target-324340836.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneId': 'Z35SXDOTRQ7X7K',
                'CreatedTime': datetime.datetime(2019, 11, 5, 16, 33, 6, 810000, tzinfo=tzutc()),
                'LoadBalancerName': 'master-target',
                'Scheme': 'internal',
                'VpcId': 'vpc-07ad4bebf61a73a1b',
                'State': {
                    'Code': 'active'
                },
                'Type': 'application',
                'AvailabilityZones': [
                    {
                        'ZoneName': 'us-east-1b',
                        'SubnetId': 'subnet-05092faa7e1cd819e',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1a',
                        'SubnetId': 'subnet-068734adb0c232409',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1c',
                        'SubnetId': 'subnet-07e5432d996cd9191',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    }
                ],
                'SecurityGroups': [
                    'sg-08c391da7b84b8f08'
                ],
                'IpAddressType': 'ipv4'
            }
        ]

    """
    elbList = get_elbv2().describe_load_balancers().get('LoadBalancers')
    return elbList


def get_application_loadbalancer(arn: str = None, name: str = None):
    """
    Get the a specific application load balancer. A name or arn must be specified for the search

    :param arn: The ARN of the load balancer
    :param name: The name  of the load balancer
    :return: `Application Load Balancer Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers>`_

    Example Output::

        [
            {
                'LoadBalancerArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:loadbalancer/app/np-load-balancer/ccad1344d28899a7',
                'DNSName': 'np-load-balancer-282693614.us-east-1.elb.amazonaws.com',
                'CanonicalHostedZoneId': 'Z35SXDOTRQ7X7K',
                'CreatedTime': datetime.datetime(2019, 10, 15, 20, 6, 42, 440000, tzinfo=tzutc()),
                'LoadBalancerName': 'np-load-balancer',
                'Scheme': 'internet-facing',
                'VpcId': 'vpc-098ec64bb7f6e4799',
                'State': {
                    'Code': 'active'
                },
                'Type': 'application',
                'AvailabilityZones': [
                    {
                        'ZoneName': 'us-east-1b',
                        'SubnetId': 'subnet-022e237798060f8de',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1c',
                        'SubnetId': 'subnet-0a0ededb6d5cec867',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    },
                    {
                        'ZoneName': 'us-east-1a',
                        'SubnetId': 'subnet-0ed958b196df664ac',
                        'LoadBalancerAddresses': [
                            {
                            }
                        ]
                    }
                ],
                'SecurityGroups': [
                    'sg-0ec1f9503c4bc5d9b'
                ],
                'IpAddressType': 'ipv4'
            }
        ]

    """

    elbList = list_application_loadbalancer()
    if name is not None:
        for elb in elbList:
            if elb.get('LoadBalancerName') == name:
                return elb
    elif arn is not None:
        for elb in elbList:
            if elb.get('LoadBalancerArn') == arn:
                return elb
    else:
        raise Exception('Either name or arn of the elb must be provided for the search')



def list_target_groups():
    """
    List all the target groups

    :return: `TargetGroups Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups>`_

    Example Output::

        [
            {
                'TargetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:targetgroup/co-app-worker-tg/59370fd540b3dcf8'
                'TargetGroupName': 'co-app-worker-tg'
                'Protocol': 'HTTPS',
                'Port': 443,
                'VpcId': 'vpc-07ad4bebf61a73a1b',
                'HealthCheckProtocol': 'HTTPS',
                'HealthCheckPort': 'traffic-port',
                'HealthCheckEnabled': True,
                'HealthCheckIntervalSeconds': 15,
                'HealthCheckTimeoutSeconds': 10,
                'HealthyThresholdCount': 2,
                'UnhealthyThresholdCount': 2,
                'HealthCheckPath': '/healthz',
                'Matcher': {
                    'HttpCode': '200-299'
                },
                'LoadBalancerArns': [
                ],
                'TargetType': 'instance'
            },
            {
                'TargetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:targetgroup/co-master-tg/24e728ee59c51f24',
                'TargetGroupName': 'co-master-tg',
                'Protocol': 'HTTPS',
                'Port': 443,
                'VpcId': 'vpc-07ad4bebf61a73a1b',
                'HealthCheckProtocol': 'HTTPS',
                'HealthCheckPort': 'traffic-port',
                'HealthCheckEnabled': True,
                'HealthCheckIntervalSeconds': 15,
                'HealthCheckTimeoutSeconds': 10,
                'HealthyThresholdCount': 2,
                'UnhealthyThresholdCount': 2,
                'HealthCheckPath': '/',
                'Matcher': {
                    'HttpCode': '200-299'
                },
                'LoadBalancerArns': [
                    'arn:aws:elasticloadbalancing:us-east-1:683863474030:loadbalancer/app/co-load-balancer/a30dcac13bc79379'
                ],
                'TargetType': 'instance'
            },
            {
                'TargetGroupArn': 'arn:aws:elasticloadbalancing:us-east-1:683863474030:targetgroup/co-worker-tg/d056707e0d7396c3',
                'TargetGroupName': 'co-worker-tg',
                'Protocol': 'HTTPS',
                'Port': 443,
                'VpcId': 'vpc-07ad4bebf61a73a1b',
                'HealthCheckProtocol': 'HTTPS',
                'HealthCheckPort': 'traffic-port',
                'HealthCheckEnabled': True,
                'HealthCheckIntervalSeconds': 30,
                'HealthCheckTimeoutSeconds': 5,
                'HealthyThresholdCount': 5,
                'UnhealthyThresholdCount': 2,
                'HealthCheckPath': '/',
                'Matcher': {
                    'HttpCode': '200'
                },
                'LoadBalancerArns': [
                ],
                'TargetType': 'instance'
            }
        ]

    """
    targetGroupList = get_elbv2().describe_target_groups().get('TargetGroups')
    return targetGroupList


def get_target_group(name: str = None, arn: str = None):
    """
    Gets a target group with a specified name or ARN
    :param name: The name of the Target Group. Required if parameter arn isn't supplied.
    :param arn: The ARN of the Target Group. Required if parameter name isn't supplied.
    :return: `TargetGroup Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups>`_
    """
    tgList = list_target_groups()
    if name is not None:
        for tg in tgList:
            if tg.get('TargetGroupName') == name:
                return tg
    elif arn is not None:
        for tg in tgList:
            if tg.get('TargetGroupArn') == arn:
                return tg
    else:
        raise Exception('Either name or arn of the target group must be provided for the search')

def add_target(port: int = None, target_name: str = None, target_arn: str = None, group_name: str = None, group_arn: str = None):
    """
    Adds a target to a target group.
    
    :param port: The port to expose the target on. Defaults to the default port of the target group.
    :param target_name: The name (tag, Key = Name) of the target instance. Required if parameter target_arn is not supplied.
    :param target_arn: The ARN of the target instance. Required if parameter target_name is not supplied.
    :param group_name: The name (tag, Key = Name) of the target group. Required if parameter group_arn is not supplied.
    :param group_arn: The ARN of the target group. Required if parameter group_name is not supplied.
    :return: If the target is successfully added to the target group.
    """
    if target_name is None and target_arn is None:
        print('must supply target name or arn')
        return False
    if group_name is None and group_arn is None:
        print('must supply group name or arn')
        return False

    # make sure the instance exists
    if target_name is not None:
        target = get_instance(target_name)
        if target is None:
            print(f"instance {target_name} not found")
            return False
    else: # arn
        target = get_instance(instance_id = target_arn)
        if target is None:
            print(f"instance {target_arn} not found")
            return False
    # make sure the target group exists
    if group_name is not None:
        group = get_target_group(group_name)
        if group is None:
            print(f"group {group_name} not found")
            return False
    else: # arn
        group = get_target_group(arn = group_arn)
        if group is None:
            print(f"group {group_arn} not found")
            return False
    # add the retrieved target to the target group
    if port is None:
        port = group['Port']
    t_param = {
        'Id': target['InstanceId'],
        'Port': port
    }
    get_elbv2().register_targets(TargetGroupArn = group['TargetGroupArn'], Targets = [t_param])

    return True

def get_targets_in_group(group_name: str = None, group_arn: str = None):
    """
    Gets a list of targets in a group.

    :param group_name: The name of the target group. Required if parameter group_arn isn't supplied.
    :param group_arn: The ARN of the target group. Required if parameter group_name isn't supplied.
    :return: A list of targets in the group.
    """

    if group_name is not None:
        group = get_target_group(group_name)
        if group is None:
            print(f"group {group_name} not found")
            return False
        group_arn = group['TargetGroupArn']
    elif group_arn is not None:
        group = get_target_group(arn = group_arn)
        if group is None:
            print(f"group {group_arn} not found")
            return False
    else:
        print('must supply group name or arn')
        return False

    return get_elbv2().describe_target_health(TargetGroupArn = group_arn)['TargetHealthDescriptions']
    

def get_elb_tags(arn: str) -> list:
    """
    Get list of tags associated with the LoadBalancer or TargetGroup

    :param arn: The ARN of the ELB
    :return: `the arn and list of tags associated with that ARN <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_tags>`_

    Example Output::

        {
                EnvType: "np"
                Name: "np-load-balancer"
        }

    """

    tagList = get_elbv2().describe_tags(ResourceArns=[arn]).get('TagDescriptions')[0].get('Tags')
    res = {}
    for x in tagList:
        key = x.get('Key')
        val = x.get('Value')
        res[key] = val
    return res

###########################################################################
# Certificate Manager
###########################################################################
def get_certs():
    """
    :return: list of certificates issued in the region, each with the keys 'CertificateARN' and 'DomainName'
    """
    return get_acm().list_certificates(CertificateStatuses = ['ISSUED'])