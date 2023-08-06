from aws.region import get_iam


###########################################################################
# IAM Roles and Profiles
###########################################################################
def list_roles(path_prefix: str = '/'):
    """
    Get list of all roles.

    Example usage::

        list_roles()
        list_roles('/aws')  For all roles prefixed with '/aws'

    :param path_prefix: `Regex <https://regex101.com/>`_ pattern for finding roles.
    :return: list of roles

    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles

    Example::

        {
            'Roles': [
                {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string',
                    'MaxSessionDuration': 123,
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                },
            ],
            'IsTruncated': True|False,
            'Marker': 'string'
        }

    """
    return get_iam().list_roles(PathPrefix=path_prefix).get('Roles')


def get_role(name: str):
    """
    Gets the specified role.

    :param name: Role name to get.
    :return: Role dictionary if found, otherwise None.
    """
    # AWS get_role() doesn't seem to work, so this is a work around.
    roles = list_roles()
    for role in roles:
        if get_role_name(role) == name:
            return role

    return None


def get_role_name(role: dict):
    """
    Extracts the RoleName from the provided dictionary.
    :param role: Role dictionary
    :return: string role name
    """
    return role.get('RoleName')


def list_profiles():
    """
    Gets the list of all instance profiles.
    :return: List of instance profile dictionaries
    """
    return get_iam().list_instance_profiles().get('InstanceProfiles')


def get_profile(name: str):
    """
    Returns the specified profile
    :param name: name of profile to get.
    :return: Profile dictionary
    """
    profiles = list_profiles()
    for profile in profiles:
        if get_profile_name(profile) == name:
            return profile

    return None


def get_profile_name(profile: dict):
    """
    Gets the InstanceProfileName from the dictionary.
    :param profile: The profile dictionary.
    :return: string profile name.
    """
    return profile.get('InstanceProfileName')