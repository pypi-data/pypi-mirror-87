import boto3
from aws.region import get_ec2, get_ssm, get_route53
import time

def list_regions():
    """
    Returns a list of dictionaries describing regions::

        [
           {
              'Endpoint':'ec2.eu-north-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'eu-north-1'
           },
           {
              'Endpoint':'ec2.ap-south-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ap-south-1'
           },
           {
              'Endpoint':'ec2.eu-west-3.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'eu-west-3'
           },
           {
              'Endpoint':'ec2.eu-west-2.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'eu-west-2'
           },
           {
              'Endpoint':'ec2.eu-west-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'eu-west-1'
           },
           {
              'Endpoint':'ec2.ap-northeast-2.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ap-northeast-2'
           },
           {
              'Endpoint':'ec2.ap-northeast-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ap-northeast-1'
           },
           {
              'Endpoint':'ec2.sa-east-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'sa-east-1'
           },
           {
              'Endpoint':'ec2.ca-central-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ca-central-1'
           },
           {
              'Endpoint':'ec2.ap-southeast-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ap-southeast-1'
           },
           {
              'Endpoint':'ec2.ap-southeast-2.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'ap-southeast-2'
           },
           {
              'Endpoint':'ec2.eu-central-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'eu-central-1'
           },
           {
              'Endpoint':'ec2.us-east-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'us-east-1'
           },
           {
              'Endpoint':'ec2.us-east-2.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'us-east-2'
           },
           {
              'Endpoint':'ec2.us-west-1.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'us-west-1'
           },
           {
              'Endpoint':'ec2.us-west-2.amazonaws.com',
              'OptInStatus':'opt-in-not-required',
              'RegionName':'us-west-2'
           }
        ]
    """
    return get_ec2().describe_regions()['Regions']


def list_azs():
    """
    Returns a list of all availability zones for current region::

        [
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1a"
                ZoneId: "use1-az4"
            }
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1b"
                ZoneId: "use1-az6"
            }
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1c"
                ZoneId: "use1-az1"
            }
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1d"
                ZoneId: "use1-az2"
            }
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1e"
                ZoneId: "use1-az3"
            }
            {
                State: "available"
                Messages: []
                RegionName: "us-east-1"
                ZoneName: "us-east-1f"
                ZoneId: "use1-az5"
            }
        ]

    """

    return get_ec2().describe_availability_zones().get('AvailabilityZones')


###########################################################################
# VPC
###########################################################################

_default_vpcid = None
_vpc_filter = None

def set_current_vpcid(vpc: dict = None, vpcid: str = None):
    """
    Sets the current VPC ID

    :param vpc: Dictionary of VPC definition, the VpcId is extracted from the passed in dictionary.
    :param vpcid: VPC Id to set it to.
    :return: No return value
    """

    global _default_vpcid
    global _vpc_filter

    if vpc:
        vpcid = get_vpcid(vpc)

    if vpcid:
        _vpc_filter = [
            {'Name': 'vpc-id', 'Values': [vpcid]}
        ]
    else:
        _vpc_filter = None

    _default_vpcid = vpcid


def get_current_vpcid():
    """
    Gets the ID of the current default VPC.
    :return: The ID of the default VPC.
    """
    global _default_vpcid

    if _default_vpcid is None:
        raise Exception("You must call set_current_vpcid() before calling get_current_vpcid()")

    return _default_vpcid


def get_vpc_filter():
    global _vpc_filter
    if _vpc_filter is None:
        raise Exception("You must call set_current_vpcid() before calling get_vpc_filter()")
    return _vpc_filter


def list_vpcs():
    """
    :return: `list of matching VPCs. <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs>`_
    """
    vpcs = get_ec2().describe_vpcs().get('Vpcs')
    return vpcs


def get_vpc(default: bool = False, name: str = None, vpcid: str = None):
    """
    Returns a dictionary describing the VPC.
    :param default: Optional - Set to true to find default VPC
    :param name: Optional - Will find VPC with matching 'Name' tag.
    :param vpcid: vpc_id to retrieve.
    :return: `Returns the dictionary of VPC info. <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs>`_
    """
    vpcs = list_vpcs()

    if default:
        for vpc in vpcs:
            if vpc['IsDefault']:
                return vpc

    elif name is not None:
        for vpc in vpcs:
            if match_tags({'Name': name}, vpc):
                return vpc

    elif vpcid is not None:
        for vpc in vpcs:
            if vpc.get('VpcId') == vpcid:
                return vpc

    else:
        raise Exception('default, name or vpcid must be provided when calling get_vpc()')
    return None


def get_vpcid(vpc: dict):
    """
    Gets the ID from a VPC dict.

    :param vpc: A dict containing information about a VPC. Usually the output of get_vpc().
    :return: The ID of the vpc
    """
    return vpc.get('VpcId')


###########################################################################
# Subnets
###########################################################################

def list_subnets(search_filter: dict = None, subnet_type: str = None):
    """
    Lists the subnets in the **current VPC** - set by set_current_vpc().  Note that the use of subnet_type
    is based on a convention to set a tag named 'SubnetType' to 'private' or 'public'
    :param search_filter: Optional dictionary of tags to filter on.
    :param subnet_type: The SubnetType tag to match on.  Typically 'private' or 'public'
    :return: `List of subnet dictionaries <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets>`_
    """
    subnets = get_ec2().describe_subnets(Filters=get_vpc_filter()).get('Subnets')

    if search_filter is not None:
        return [
            subnet
            for subnet in subnets
            if match_tags(search_filter, subnet)
        ]

    if subnet_type is not None:
        return [
            subnet
            for subnet in subnets
            if match_tags({'SubnetType': subnet_type}, subnet)
        ]

    return subnets


def get_subnet(subnet_id: str):
    """
    Returns the specified subnet - must be in the current VPC specified by set_current_vpcid()
    :param subnet_id: The subnet ID to get.
    :return: `Subnet Details <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets>`_
    """
    subnets = list_subnets()
    for subnet in subnets:
        if subnet.get('SubnetId') == subnet_id:
            return subnet

    return None


def get_subnet_id(subnet: dict):
    """
    Convenience function to extract subnet ID from subnet dictionary.
    :param subnet: Subnet dictionary returned by get_subnet() or list_subnets()
    :return: subnet ID.
    """

    return subnet.get('SubnetId')


###########################################################################
# Internet Gateways & NATs
###########################################################################

def list_igws():
    """
    Since internet gateways can be created without attaching to a VPC, we will
    list all internet gateways instead of constraining it by current VPC.  To get
    the gateway associated with the current VPC, use get_vpc_igw().

    :return: All gateways on the current account.

    Example output::

        [
            {
                Attachments: [
                    {
                        State: "available"
                        VpcId: "vpc-08bc3183e3bc9e88e"
                    }
                ]
                InternetGatewayId: "igw-0762e46a2c4fdcf49"
                OwnerId: "862586795542"
                Tags: [
                    {
                        Key: "aws:cloudformation:logical-id"
                        Value: "RancherInternetGateway"
                    }
                    {
                        Key: "aws:cloudformation:stack-id"
                        Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-00-rancher-vpc/96979170-fcb0-11e9-99cd-0ad7a569cb8c"
                    }
                    {
                        Key: "Name"
                        Value: "unit-igw"
                    }
                    {
                        Key: "aws:cloudformation:stack-name"
                        Value: "unit-00-rancher-vpc"
                    }
                    {
                        Key: "EnvType"
                        Value: "unit"
                    }
                ]
            }
            {
                Attachments: [
                    {
                        State: "available"
                        VpcId: "vpc-77777b1f"
                    }
                ]
                InternetGatewayId: "igw-1a63cd72"
                OwnerId: "862586795542"
                Tags: []
            }
        ]
    """
    return get_ec2().describe_internet_gateways().get('InternetGateways')

def get_vpc_igw():
    """
    Finds the Internet Gateway attached to the current VPC (set_current_vpcid()).
    There can only be one Internet Gatway per VPC.

    :return: Internet gateway dictionary if found, otherwise None
    """
    igws = list_igws()
    curr_vpcid = get_current_vpcid()

    for igw in igws:
        attachments = igw.get('Attachments')
        if attachments is None:
            continue

        for attachment in attachments:
            if curr_vpcid == attachment.get('VpcId'):
                return igw

    return None

def list_nats():
    """
    Listsd the NAT gateways associated with the current VPC.

    :return: list of dictionary NAT definitions

    Example Output::

        [
            {
                CreateTime: 2019-11-01 14:05:36+00:00
                NatGatewayAddresses: [
                    {
                        AllocationId: "eipalloc-057df1367493b074f"
                        NetworkInterfaceId: "eni-05558f734b0f69a1a"
                        PrivateIp: "10.222.0.201"
                        PublicIp: "3.133.209.133"
                    }
                ]
                NatGatewayId: "nat-0c1b32ec7ec590672"
                State: "available"
                SubnetId: "subnet-0e0ce7e00767ea044"
                VpcId: "vpc-08bc3183e3bc9e88e"
                Tags: [
                    {
                        Key: "aws:cloudformation:stack-name"
                        Value: "unit-00-rancher-vpc"
                    }
                    {
                        Key: "aws:cloudformation:logical-id"
                        Value: "NAT1"
                    }
                    {
                        Key: "aws:cloudformation:stack-id"
                        Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-00-rancher-vpc/96979170-fcb0-11e9-99cd-0ad7a569cb8c"
                    }
                    {
                        Key: "EnvType"
                        Value: "unit"
                    }
                    {
                        Key: "Name"
                        Value: "unit-nat-1"
                    }
                ]
            }
        ]

    """
    return get_ec2().describe_nat_gateways(Filters=get_vpc_filter())['NatGateways']



def list_eips():
    """
    Lists all Elastic IPs on the account.
    :return: List of dictionary definitions of all Elastic IPs.

    Example Output::

        [
            {
                PublicIp: "3.133.209.133"
                AllocationId: "eipalloc-057df1367493b074f"
                AssociationId: "eipassoc-03ebeb8f838a36e24"
                Domain: "vpc"
                NetworkInterfaceId: "eni-05558f734b0f69a1a"
                NetworkInterfaceOwnerId: "862586795542"
                PrivateIpAddress: "10.222.0.201"
                PublicIpv4Pool: "amazon"
            }
        ]
    """
    return get_ec2().describe_addresses()['Addresses']


def release_eip(allocation_id: str):
    """
    Releases an Elastic IP

    :param id: The AllocationId of the Elastic IP to delete
    :return: None
    """
    get_ec2().release_address(AllocationId=allocation_id)


def release_unused_eips():
    """
    Releases all unused Elastic IPs (those with no associated instance).

    :return: None
    """
    for eip in list_eips():
        if 'InstanceId' not in eip:
            release_eip(eip['AllocationId'])


###########################################################################
# Route Tables
###########################################################################

def list_route_tables(search_filter: dict = None):
    """
    List all route tables associated with the current VPC.

    :param search_filter: A dictionary with name/value pairs that we want to filter on.
    :return: `List of dictionaries describing each route table <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-route-tables.html>`_

    Example Output::

        [
            {
                Associations: [
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-048a2aa4644bf03cc"
                        RouteTableId: "rtb-089d21cede2d7cb49"
                        SubnetId: "subnet-0d1208fb2f4737bda"
                    }
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-05ab66b97ec489fb9"
                        RouteTableId: "rtb-089d21cede2d7cb49"
                        SubnetId: "subnet-02ddb6efaea798c96"
                    }
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-0632e1115b7cefdc4"
                        RouteTableId: "rtb-089d21cede2d7cb49"
                        SubnetId: "subnet-020c75d83b72395c7"
                    }
                ]
                PropagatingVgws: []
                RouteTableId: "rtb-089d21cede2d7cb49"
                Routes: [
                    {
                        DestinationCidrBlock: "10.222.0.0/16"
                        GatewayId: "local"
                        Origin: "CreateRouteTable"
                        State: "active"
                    }
                    {
                        DestinationCidrBlock: "0.0.0.0/0"
                        NatGatewayId: "nat-0c1b32ec7ec590672"
                        Origin: "CreateRoute"
                        State: "active"
                    }
                ]
                Tags: [
                    {
                        Key: "aws:cloudformation:stack-id"
                        Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-00-rancher-vpc/96979170-fcb0-11e9-99cd-0ad7a569cb8c"
                    }
                    {
                        Key: "Name"
                        Value: "unit-private-rt"
                    }
                    {
                        Key: "EnvType"
                        Value: "unit"
                    }
                    {
                        Key: "aws:cloudformation:stack-name"
                        Value: "unit-00-rancher-vpc"
                    }
                    {
                        Key: "aws:cloudformation:logical-id"
                        Value: "PrivateRouteTable"
                    }
                ]
                VpcId: "vpc-08bc3183e3bc9e88e"
                OwnerId: "862586795542"
            }
            {
                Associations: [
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-078a89ddf97cdc8e0"
                        RouteTableId: "rtb-091cdf2db7b580a9c"
                        SubnetId: "subnet-039edc65f3dec70e0"
                    }
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-060b9faa4015ff29e"
                        RouteTableId: "rtb-091cdf2db7b580a9c"
                        SubnetId: "subnet-0e0ce7e00767ea044"
                    }
                    {
                        Main: False
                        RouteTableAssociationId: "rtbassoc-013b16e1af58d02ab"
                        RouteTableId: "rtb-091cdf2db7b580a9c"
                        SubnetId: "subnet-0c5309df5bb0dafc6"
                    }
                ]
                PropagatingVgws: []
                RouteTableId: "rtb-091cdf2db7b580a9c"
                Routes: [
                    {
                        DestinationCidrBlock: "10.222.0.0/16"
                        GatewayId: "local"
                        Origin: "CreateRouteTable"
                        State: "active"
                    }
                    {
                        DestinationCidrBlock: "0.0.0.0/0"
                        GatewayId: "igw-0762e46a2c4fdcf49"
                        Origin: "CreateRoute"
                        State: "active"
                    }
                ]
                Tags: [
                    {
                        Key: "Name"
                        Value: "unit-public-rt"
                    }
                    {
                        Key: "aws:cloudformation:stack-name"
                        Value: "unit-00-rancher-vpc"
                    }
                    {
                        Key: "aws:cloudformation:stack-id"
                        Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-00-rancher-vpc/96979170-fcb0-11e9-99cd-0ad7a569cb8c"
                    }
                    {
                        Key: "aws:cloudformation:logical-id"
                        Value: "PublicRouteTable"
                    }
                    {
                        Key: "EnvType"
                        Value: "unit"
                    }
                ]
                VpcId: "vpc-08bc3183e3bc9e88e"
                OwnerId: "862586795542"
            }
            {
                Associations: [
                    {
                        Main: True
                        RouteTableAssociationId: "rtbassoc-098aab5b617465c86"
                        RouteTableId: "rtb-0142fd63a657ef8cf"
                    }
                ]
                PropagatingVgws: []
                RouteTableId: "rtb-0142fd63a657ef8cf"
                Routes: [
                    {
                        DestinationCidrBlock: "10.222.0.0/16"
                        GatewayId: "local"
                        Origin: "CreateRouteTable"
                        State: "active"
                    }
                ]
                Tags: []
                VpcId: "vpc-08bc3183e3bc9e88e"
                OwnerId: "862586795542"
            }
        ]
    """
    rts = get_ec2().describe_route_tables(Filters=get_vpc_filter())['RouteTables']

    if search_filter is not None:
        return [
            rt
            for rt in rts
            if match_tags(search_filter, rt)
        ]

    return rts


def get_route_table(name: str = None, rt_id: str = None, subnet_id: str = None):
    """
    Get a route table by name: `get_route_table('dev-public-rt')`
    Get a route table by route table ID: `get_route_table(rt_id= 'rtb-091cdf2db7b580a9c')`
    get a route table by associated subnet ID: `get_route_table(subnet_id= 'subnet-039edc65f3dec70e0')`
    :param name: Name tag to search for.
    :param rt_id: Route table ID to search for.
    :param subnet_id: associated Subnet ID to search route table for.
    :return: `dictionary describing the subnet <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-route-tables.html>`_

    Example Output::

            {
            Associations: [
                {
                    Main: False
                    RouteTableAssociationId: "rtbassoc-048a2aa4644bf03cc"
                    RouteTableId: "rtb-089d21cede2d7cb49"
                    SubnetId: "subnet-0d1208fb2f4737bda"
                }
                {
                    Main: False
                    RouteTableAssociationId: "rtbassoc-05ab66b97ec489fb9"
                    RouteTableId: "rtb-089d21cede2d7cb49"
                    SubnetId: "subnet-02ddb6efaea798c96"
                }
                {
                    Main: False
                    RouteTableAssociationId: "rtbassoc-0632e1115b7cefdc4"
                    RouteTableId: "rtb-089d21cede2d7cb49"
                    SubnetId: "subnet-020c75d83b72395c7"
                }
            ]
            PropagatingVgws: []
            RouteTableId: "rtb-089d21cede2d7cb49"
            Routes: [
                {
                    DestinationCidrBlock: "10.222.0.0/16"
                    GatewayId: "local"
                    Origin: "CreateRouteTable"
                    State: "active"
                }
                {
                    DestinationCidrBlock: "0.0.0.0/0"
                    NatGatewayId: "nat-0c1b32ec7ec590672"
                    Origin: "CreateRoute"
                    State: "active"
                }
            ]
            Tags: [
                {
                    Key: "aws:cloudformation:stack-id"
                    Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-00-rancher-vpc/96979170-fcb0-11e9-99cd-0ad7a569cb8c"
                }
                {
                    Key: "Name"
                    Value: "unit-private-rt"
                }
                {
                    Key: "EnvType"
                    Value: "unit"
                }
                {
                    Key: "aws:cloudformation:stack-name"
                    Value: "unit-00-rancher-vpc"
                }
                {
                    Key: "aws:cloudformation:logical-id"
                    Value: "PrivateRouteTable"
                }
            ]
            VpcId: "vpc-08bc3183e3bc9e88e"
            OwnerId: "862586795542"
        }

    """
    rts = list_route_tables()

    if name is not None:
        for rt in rts:
            if match_tags({'Name': name}, rt):
                return rt

    elif rt_id is not None:
        for rt in rts:
            if rt_id == rt.get('RouteTableId'):
                return rt

    elif subnet_id is not None:
        for rt in rts:
            associations = rt.get('Associations')
            if associations is None:
                return None

            for association in associations:
                if subnet_id == association.get('SubnetId'):
                    return rt

    else:
        raise Exception('name, rt_id or subnet_id must be specified when calling get_route_table()')

    return None


def get_route_table_id(rt: dict):
    """
    Extract RouteTableId from the route table dictionary definition.
    :param rt: dictionary of route table definition.
    :return: string route table ID
    """
    return rt.get('RouteTableId')

###########################################################################
# Security Groups
###########################################################################

def list_sgs(search_filter: dict = None):
    """
    :return: Array of `Security Group Information <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-security-groups.html>`_
    """
    sgs = get_ec2().describe_security_groups(Filters=get_vpc_filter())['SecurityGroups']

    if search_filter is not None:
        return [
            sg
            for sg in sgs
            if match_tags(search_filter, sg)
        ]
    return sgs


def get_sg(name: str = None, sgid: str = None):
    """
    Gets a security group by Name tag or security group ID.
    :param name: Name tag to search for.
    :param sgid: Security group ID to search for.
    :return: dictionary with `Security Group Information <https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-security-groups.html>`_

    Example output::

        {
            "SecurityGroups": [
                {
                    "IpPermissionsEgress": [],
                    "Description": "My security group",
                    "IpPermissions": [
                        {
                            "PrefixListIds": [],
                            "FromPort": 22,
                            "IpRanges": [
                                {
                                    "CidrIp": "203.0.113.0/24"
                                }
                            ],
                            "ToPort": 22,
                            "IpProtocol": "tcp",
                            "UserIdGroupPairs": []
                        }
                    ],
                    "GroupName": "MySecurityGroup",
                    "OwnerId": "123456789012",
                    "GroupId": "sg-903004f8",
                }
            ]
        }
    """
    sgs = list_sgs()

    if name is not None:
        for sg in sgs:
            if match_tags({'Name': name}, sg):
                return sg

    elif sgid is not None:
        for sg in sgs:
            if sg.get('GroupId') == sgid:
                return sg

    else:
        raise Exception('You must provide name or sgid')

    return None


def get_sgid(sg: dict):
    """
    Returns the security group ID (GroupId)
    :param sg: The dictionary for the security group
    :return: string security group ID
    """
    return sg.get('GroupId')
###########################################################################
# KeyPairs
###########################################################################

def create_key_pair(name: str):
    """
    Creates a KeyPair - this function will not do anything if
    keypair already exists.

    This function is primarily for **testing purposes**.  We discourage
    creating keypairs and transfering private keys to other machines as
    this has the potential to expose private keys.  It is better to create
    the keypair on the machine where the private key will reside and only
    import the public key to AWS.

    :param name: Name of keypair to create
    :return: None if keypair already exists, otherwise a dict.

    Example return value::

        {
            'KeyFingerprint': 'string',
            'KeyMaterial': 'string',
            'KeyName': 'string'
        }

    Note that KeyMaterial is an unencrypted PEM file.
    """
    if key_pair_exists(name):
        return None

    return get_ec2().create_key_pair(KeyName=name)


def list_key_pairs(name: str = None):
    """
    Lists the names of key pairs in the AWS account.
    :param name: If provided, only return key pairs with this name. Should return a list with a single entry if it exists.
    :return: a list of key pairs, either in the account or that match the name.
    """
    kps = get_ec2().describe_key_pairs().get('KeyPairs')
    if name is not None:
        return [
            kp
            for kp in kps
            if kp.get('KeyName') == name
        ]

    return kps


def key_pair_exists(name: str):
    """
    Finds if a key pair exists.

    :param name: The name of the sought key pair
    :return: True if there is a key pair with the provided name.
    """
    kps = list_key_pairs(name)
    return len(kps) > 0


def delete_key_pair(name: str):
    """
    Deletes a key pair record if it exists.

    :param name: The name of the key pair to delete.
    :return: None if the key pair does not exist. Returns metadata about the deletion if it does.
    """
    if key_pair_exists(name):
        return get_ec2().delete_key_pair(KeyName=name)
    else:
        return None

def wait_for_key_pair(name: str, interval: int = 10, timeout: int = 120):
    """
    Waits for a key pair to exist.

    :param name: The name of the key pair we're waiting on.
    :param interval: How often to check if the key pair exists (in seconds).
    :param timeout: How long to wait before we time out (in seconds).
    :return: True if the key pair exists and we don't timed out. False if we time out.
    """
    for i in range(timeout // interval + 1):
            if key_pair_exists(name):
                return True
            if i <= timeout // interval:
                print(f'waiting for key_pair {name}')
                time.sleep(interval)
    return False

###########################################################################
# AMIs
###########################################################################

def get_linux2_ami():
    """
    Gets the AMI for the latest HVM x64 version of Amazon Linux 2
    
    :return: The AMI for the lastest Amazon Linux 2 release.
    """
    response = get_ec2().describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [
                    'amzn2-ami-hvm-2.0.????????-x86_64-gp2',
                ]
            },
            {
                'Name': 'state',
                'Values': [
                    'available',
                ]
            },

        ],
        Owners=['amazon']
    )['Images']

    latest = None
    imageid = None
    for ami in response:
        created = ami['CreationDate']
        if latest is None or created > latest:
            latest = created
            imageid = ami['ImageId']

    return imageid


def get_image(imageid: str):
    """
    Gets details about an image.

    :param imageid: The ID of the image you're querying for.
    :return: Details about the image. See `boto3's docs <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images>`_ for more details.
    """
    response = get_ec2().describe_images(
        ImageIds=[imageid]
    )['Images']

    if response is None or len(response) < 1:
        return None

    return response


###########################################################################
# EC2 Instances
###########################################################################

def list_instances(search_filter: dict = None):
    """
    Lists all instances.  If filter is provided, returns all instances that match the criteria.
    :param search_filter: Name value pair of tags to filter on.  This is an AND operation.
    :return: List of instance dictionaries.

    Example Output::

        [
            {
                AmiLaunchIndex: 0
                ImageId: "ami-02bcbb802e03574ba"
                InstanceId: "i-0f49c699d49588ddd"
                InstanceType: "t3a.micro"
                KeyName: "unit-key_pair"
                LaunchTime: 2019-11-01 16:19:50+00:00
                Monitoring: {
                    State: "disabled"
                }
                Placement: {
                    AvailabilityZone: "us-east-2a"
                    GroupName: ""
                    Tenancy: "default"
                }
                PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
                PrivateIpAddress: "10.222.0.80"
                ProductCodes: []
                PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
                PublicIpAddress: "3.133.124.106"
                State: {
                    Code: 16
                    Name: "running"
                }
                StateTransitionReason: ""
                SubnetId: "subnet-0e0ce7e00767ea044"
                VpcId: "vpc-08bc3183e3bc9e88e"
                Architecture: "x86_64"
                BlockDeviceMappings: [
                    {
                        DeviceName: "/dev/xvda"
                        Ebs: {
                            AttachTime: 2019-11-01 16:19:51+00:00
                            DeleteOnTermination: True
                            Status: "attached"
                            VolumeId: "vol-0130fd9eff3712222"
                        }
                    }
                ]
                ClientToken: "unit-Basti-1TJ3F74Z82AXK"
                EbsOptimized: False
                EnaSupport: True
                Hypervisor: "xen"
                NetworkInterfaces: [
                    {
                        Association: {
                            IpOwnerId: "amazon"
                            PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
                            PublicIp: "3.133.124.106"
                        }
                        Attachment: {
                            AttachTime: 2019-11-01 16:19:50+00:00
                            AttachmentId: "eni-attach-0dd31d7d64d5d3d8e"
                            DeleteOnTermination: True
                            DeviceIndex: 0
                            Status: "attached"
                        }
                        Description: ""
                        Groups: [
                            {
                                GroupName: "unit-01-rancher-bastion-BastionSg-5Q84EII1WCHI"
                                GroupId: "sg-094bd5d8b7a6a51b9"
                            }
                        ]
                        Ipv6Addresses: []
                        MacAddress: "02:71:8a:a9:0a:6a"
                        NetworkInterfaceId: "eni-06091db55e45239d2"
                        OwnerId: "862586795542"
                        PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
                        PrivateIpAddress: "10.222.0.80"
                        PrivateIpAddresses: [
                            {
                                Association: {
                                    IpOwnerId: "amazon"
                                    PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
                                    PublicIp: "3.133.124.106"
                                }
                                Primary: True
                                PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
                                PrivateIpAddress: "10.222.0.80"
                            }
                        ]
                        SourceDestCheck: True
                        Status: "in-use"
                        SubnetId: "subnet-0e0ce7e00767ea044"
                        VpcId: "vpc-08bc3183e3bc9e88e"
                        InterfaceType: "interface"
                    }
                ]
                RootDeviceName: "/dev/xvda"
                RootDeviceType: "ebs"
                SecurityGroups: [
                    {
                        GroupName: "unit-01-rancher-bastion-BastionSg-5Q84EII1WCHI"
                        GroupId: "sg-094bd5d8b7a6a51b9"
                    }
                ]
                SourceDestCheck: True
                Tags: [
                    {
                        Key: "Name"
                        Value: "unit-bastion"
                    }
                    {
                        Key: "aws:cloudformation:stack-name"
                        Value: "unit-01-rancher-bastion"
                    }
                    {
                        Key: "EnvType"
                        Value: "unit"
                    }
                    {
                        Key: "aws:cloudformation:logical-id"
                        Value: "Bastion"
                    }
                    {
                        Key: "aws:cloudformation:stack-id"
                        Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-01-rancher-bastion/67a687a0-fcc3-11e9-a0d8-0ade6091f9d8"
                    }
                    {
                        Key: "CreatedBy"
                        Value: "862586795542"
                    }
                ]
                VirtualizationType: "hvm"
                CpuOptions: {
                    CoreCount: 1
                    ThreadsPerCore: 2
                }
                CapacityReservationSpecification: {
                    CapacityReservationPreference: "open"
                }
                HibernationOptions: {
                    Configured: False
                }
            }
        ]

    """
    reservations = get_ec2().describe_instances(Filters=get_vpc_filter())['Reservations']

    instances = []
    for reservation in reservations:
        instances.extend(reservation.get('Instances'))

    if search_filter is not None:
        return [
            instance
            for instance in instances
            if match_tags(search_filter, instance)
        ]

    return instances


def get_instance(name: str = None, instance_id: str = None):
    """
    Gets the specified instance.  You must specify a name or instance_id::

        get_instance('unit-bastion')   // default search by name.
        get_instance(name='unit-bastion')
        get_instance(instance_id='i-124124124123')

    :param name: Name tag to search for.
    :param instance_id: Instance ID to search for.

    :return: Returns instance ID if found, otherwise None.

    Only returns one entry.  If multiple entries are expected, use list_instances().

    Example Output::

        {
            AmiLaunchIndex: 0
            ImageId: "ami-02bcbb802e03574ba"
            InstanceId: "i-0f49c699d49588ddd"
            InstanceType: "t3a.micro"
            KeyName: "unit-key_pair"
            LaunchTime: 2019-11-01 16:19:50+00:00
            Monitoring: {
                State: "disabled"
            }
            Placement: {
                AvailabilityZone: "us-east-2a"
                GroupName: ""
                Tenancy: "default"
            }
            PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
            PrivateIpAddress: "10.222.0.80"
            ProductCodes: []
            PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
            PublicIpAddress: "3.133.124.106"
            State: {
                Code: 16
                Name: "running"
            }
            StateTransitionReason: ""
            SubnetId: "subnet-0e0ce7e00767ea044"
            VpcId: "vpc-08bc3183e3bc9e88e"
            Architecture: "x86_64"
            BlockDeviceMappings: [
                {
                    DeviceName: "/dev/xvda"
                    Ebs: {
                        AttachTime: 2019-11-01 16:19:51+00:00
                        DeleteOnTermination: True
                        Status: "attached"
                        VolumeId: "vol-0130fd9eff3712222"
                    }
                }
            ]
            ClientToken: "unit-Basti-1TJ3F74Z82AXK"
            EbsOptimized: False
            EnaSupport: True
            Hypervisor: "xen"
            NetworkInterfaces: [
                {
                    Association: {
                        IpOwnerId: "amazon"
                        PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
                        PublicIp: "3.133.124.106"
                    }
                    Attachment: {
                        AttachTime: 2019-11-01 16:19:50+00:00
                        AttachmentId: "eni-attach-0dd31d7d64d5d3d8e"
                        DeleteOnTermination: True
                        DeviceIndex: 0
                        Status: "attached"
                    }
                    Description: ""
                    Groups: [
                        {
                            GroupName: "unit-01-rancher-bastion-BastionSg-5Q84EII1WCHI"
                            GroupId: "sg-094bd5d8b7a6a51b9"
                        }
                    ]
                    Ipv6Addresses: []
                    MacAddress: "02:71:8a:a9:0a:6a"
                    NetworkInterfaceId: "eni-06091db55e45239d2"
                    OwnerId: "862586795542"
                    PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
                    PrivateIpAddress: "10.222.0.80"
                    PrivateIpAddresses: [
                        {
                            Association: {
                                IpOwnerId: "amazon"
                                PublicDnsName: "ec2-3-133-124-106.us-east-2.compute.amazonaws.com"
                                PublicIp: "3.133.124.106"
                            }
                            Primary: True
                            PrivateDnsName: "ip-10-222-0-80.us-east-2.compute.internal"
                            PrivateIpAddress: "10.222.0.80"
                        }
                    ]
                    SourceDestCheck: True
                    Status: "in-use"
                    SubnetId: "subnet-0e0ce7e00767ea044"
                    VpcId: "vpc-08bc3183e3bc9e88e"
                    InterfaceType: "interface"
                }
            ]
            RootDeviceName: "/dev/xvda"
            RootDeviceType: "ebs"
            SecurityGroups: [
                {
                    GroupName: "unit-01-rancher-bastion-BastionSg-5Q84EII1WCHI"
                    GroupId: "sg-094bd5d8b7a6a51b9"
                }
            ]
            SourceDestCheck: True
            Tags: [
                {
                    Key: "Name"
                    Value: "unit-bastion"
                }
                {
                    Key: "aws:cloudformation:stack-name"
                    Value: "unit-01-rancher-bastion"
                }
                {
                    Key: "EnvType"
                    Value: "unit"
                }
                {
                    Key: "aws:cloudformation:logical-id"
                    Value: "Bastion"
                }
                {
                    Key: "aws:cloudformation:stack-id"
                    Value: "arn:aws:cloudformation:us-east-2:862586795542:stack/unit-01-rancher-bastion/67a687a0-fcc3-11e9-a0d8-0ade6091f9d8"
                }
                {
                    Key: "CreatedBy"
                    Value: "862586795542"
                }
            ]
            VirtualizationType: "hvm"
            CpuOptions: {
                CoreCount: 1
                ThreadsPerCore: 2
            }
            CapacityReservationSpecification: {
                CapacityReservationPreference: "open"
            }
            HibernationOptions: {
                Configured: False
            }
        }
    """
    instances = list_instances()

    if name is not None:
        for instance in instances:
            if name == get_tag_value(instance, 'Name'):
                return instance

    elif instance_id is not None:
        for instance in instances:
            if instance_id == instance.get('InstanceId'):
                return instance

    else:
        raise Exception('name or instance_id must be provided for get_instance()')

    return None


def get_instance_id(instance: dict):
    """
    Gets the instance ID from the dictionary that is passed in.
    :param instance: dictionary instance information
    :return: string instance ID
    """
    return instance.get('InstanceId')


###########################################################################
# Tags
###########################################################################

def get_tag_value(aws_obj: dict, key: str):
    """
    Gets the tag value for the specified key from the specified aws object

    :param aws_obj: Object to query for Tag element
    :param key: Key to query on for the value
    :return: Value of specified key.
    """
    tags = aws_obj.get('Tags')
    for tag in tags:
        if tag.get('Key') == key:
            return tag.get('Value')
    return None


def get_ec2_tags(aws_obj: dict = None, name: str = None, instance_id: str = None):
    """
    Returns the tags in a standard dictionary format, simplified from the
    original AWS Tags format.

    The AWS object would look something like this (note Tags format)::

        {
            'Name': 'default-vpc',
            'State': 'available',
            'Tags': [
                { 'Key': 'Name', 'Value': 'default-vpc'},
                { 'Key': 'EnvType', 'Value': 'dev'}
            ],
            'VpcId': 'vpc-b43582ce'
        }

    :param aws_obj: The AWS object we are extracting the 'Tags' from.
    :return:  A simplified dictionary containing name value pairs::

        { 'Name': 'default-vpc', 'EnvType': 'dev' }

    """

    if name:
        aws_obj = get_instance(name = name)
    elif instance_id:
        aws_obj = get_instance(instance_id = instance_id)

    tags = aws_obj.get('Tags')

    if tags is None:
        return {}

    return {
        tag['Key']: tag['Value']
        for tag in tags
    }


def match_tags(tags: dict, aws_obj: dict):
    """
    This function compares a collection of tags to those on an EC2 resource. If the object does not have
    a tag present in the supplied collection or the two tags' values don't match, this returns false.

    :param tags: A collection of key/value pairs to compare to a resource's tags.
    :param aws_obj: the object with tags we are comparing to the first parameter's key/value pairs.
    :return: if all keys in tags are present in aws_obj and have the same value as in tags.
    """

    obj_tags = get_ec2_tags(aws_obj)

    for key in tags.keys():
        if obj_tags.get(key) is None:
            return False

        if tags[key] != obj_tags[key]:
            return False

    return True

def set_tag(key: str, value: str, name: str = None, instance_id: str = None):
    """
    Sets a tag for an EC2 instance to a given value.

    :param key: The tag key to set
    :param value: The new/updated tag's value
    :param name: The instance's name. Required if parameter instance_id is not supplied.
    :param instance_id: The instance's id. Required if parameter name is not supplied.
    :return: True if the instance is successfully updated with a tag key = value.
             None if both name and id are missing or if the corresponding instance doesn't exist.
    """
    if name is None and instance_id is None:
        print('Must supply an instance name or id to tag')
        return None
    instance = get_instance(name = name, instance_id = instance_id)
    if instance == None:
        return None
    tag = {
      'Key': key,
      'Value': value
    }
    get_ec2().create_tags(Resources = [get_instance_id(instance)], Tags = [tag])
    return True
    

def wait_for_ready(name: str = None, instance_id: str = None, interval: int = 10, timeout: int = 120):
    """
    Waits for an instance to have a tag "Ready" with the value True. We set that tag at the end of each
    instance's UserData/startup script, which lets us know that all software has finished installing.

    :param name: The instance's name. Required if parameter instance_id is not supplied.
    :param instance_id: The instance's id. Required if parameter name is not supplied.
    :param interval: This function polls the instance every [interval] seconds. Defaults to 10.
    :param timeout: After [timeout] seconds, the function returns False. Defaults to 120.
    :return: True once the instance is ready. False if the instance is not ready by the time we hit timeout.
             None if name and id are not supplied or if the corresponding instance doesn't exist.
    """
    if name is None and instance_id is None:
       print('Must supply an instance name or id to wait on')
       return None
    instance = None
    instance = get_instance(name = name, instance_id = instance_id)
    if instance is None:
        print(f'Instance not found: {name} / {instance_id}')
        return None
    for i in range(timeout // interval + 1):
        ready = get_tag_value(instance, 'Ready')
        if ready == 'True' or ready == 'true' or ready == True:
            return True
        if i <= timeout // interval:
            print(f'waiting for {get_instance_id(instance)} to be ready')
            time.sleep(interval)
            instance = get_instance(instance_id = get_instance_id(instance))
    return False


###########################################################################
# SSM
###########################################################################

def ssm_run_shell_script(name: str = None, instance_id: str = None, commands = [], directory: str = '/home/ec2-user/', comment: str = 'Ran a shell script'):
    """
    Runs a shell script on an instance via secure systems manager. If the instance does not
    have the proper SSM permissions, the call will fail. Note that this does not wait for the
    script to finish executing; if you want to do that, we recommend starting and ending the
    script with API calls setting the 'Ready' tag to False and True respectively. That way,
    you can follow up the call with the wait_for_ready() function.

    :param name: The instance's name. Required if parameter instance_id is not supplied.
    :param instance_id: The instance's id. Required if parameter name is not supplied.
    :param commands: A list containing commands to execute. Each line of the sequence should be a string in the list.
    :param directory: The directory to execute the script from. Defaults to ec2-user's home directory.
    :param comment: A comment to attach to the command. Visible on the AWS web console in command history. Defaults to 'Ran a shell script'.
    :return: The response from AWS to the command. See `the boto3 docs <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command>`_ for spec.
    """
    if instance_id is not None:
        iid = instance_id
    elif name:
        iid = get_instance_id(get_instance(name))
    if iid is None:
        print('Must specify an instance to run the script on')
        return None
    response = get_ssm().send_command(
        InstanceIds = [iid],
        DocumentName = 'AWS-RunShellScript',
        Comment = comment,
        Parameters = {
          'commands': commands,
          'workingDirectory': [directory]
        }
    )
    return response

###########################################################################
# Route53
###########################################################################
def list_hosted_zones():
    """
    Returns a list of hosted zones. Useful data the list contains are hosted zone IDs and their (domain) names.
    Note that hosted zones are not region-bound.
    
    :return: a list of hosted zones as dicts with the following format: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
    """
    return get_route53().list_hosted_zones().get('HostedZones', [])

def get_zone_vpc_ids(zone_id: str):
    """
    Returns a list of VPC ids associated with a given hosted zone

    :param id: The id of the hosted zone
    :return: a list of VPC id strings associated with that hosted zone
    """
    vpcs = get_route53().get_hosted_zone(Id = zone_id).get('VPCs', [])
    return [
      vpc.get('VPCId')
      for vpc in vpcs
    ]