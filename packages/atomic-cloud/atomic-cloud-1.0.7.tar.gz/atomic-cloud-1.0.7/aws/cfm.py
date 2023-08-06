import os
import sys
import time
import itertools

import boto3
from botocore.exceptions import ClientError
from jinja2 import Environment, Template, FileSystemLoader

from po.pretty_object import PrettyObject
from aws import region

###############################################################################
# CloudFormation
###############################################################################

# Stack Status Values
CREATE_COMPLETE = 'CREATE_COMPLETE'
CREATE_IN_PROGRESS = 'CREATE_IN_PROGRESS'
CREATE_FAILED = 'CREATE_FAILED'
ROLLBACK_IN_PROGRESS = 'ROLLBACK_IN_PROGRESS'
ROLLBACK_FAILED = 'ROLLBACK_FAILED'
ROLLBACK_COMPLETE = 'ROLLBACK_COMPLETE'
DELETE_IN_PROGRESS = 'DELETE_IN_PROGRESS'
DELETE_FAILED = 'DELETE_FAILED'
DELETE_COMPLETE = 'DELETE_COMPLETE'
UPDATE_IN_PROGRESS = 'UPDATE_IN_PROGRESS'
UPDATE_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_COMPLETE = 'UPDATE_COMPLETE'
UPDATE_ROLLBACK_IN_PROGRESS = 'UPDATE_ROLLBACK_IN_PROGRESS'
UPDATE_ROLLBACK_FAILED = 'UPDATE_ROLLBACK_FAILED'
UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_ROLLBACK_COMPLETE = 'UPDATE_ROLLBACK_COMPLETE'
REVIEW_IN_PROGRESS = 'REVIEW_IN_PROGRESS'

# Capability Values
CAPABILITY_IAM = 'CAPABILITY_IAM'
CAPABILITY_NAMED_IAM = 'CAPABILITY_NAMED_IAM'
CAPABILITY_AUTO_EXPAND = 'CAPABILITY_AUTO_EXPAND'

po = PrettyObject()

def list_stacks(stack_status_filter=None):
    """
    Gets a list of all stacks.
    
    :param stack_status_filter: The list of stack status types to include (if not present, all types are included)
    :return: a list of all stack summaries or None if the filter was bad
    """
    client = region.get_cloudformation()
    if type(stack_status_filter) is str:
        stack_status_filter = [stack_status_filter]  # handles single filter as string
    stacks_remain = True
    all_stacks = []
    token = None
    try:
        while stacks_remain:
            if token and stack_status_filter:
                stacks = client.list_stacks(StackStatusFilter=stack_status_filter, NextToken=token)
            elif stack_status_filter:
                stacks = client.list_stacks(StackStatusFilter=stack_status_filter)
            elif token:
                stacks = client.list_stacks(NextToken=token)
            else:
                stacks = client.list_stacks()
            all_stacks.extend(stacks['StackSummaries'])
            if 'NextToken' in stacks:
                token = stacks['NextToken']
            stacks_remain = 'NextToken' in stacks
    except ClientError:
        return []
    return all_stacks


def describe_stacks(stack_name=None):
    """
    Describes all stacks (or one with a given name)
    
    :param stack_name: The name or ID of the stack you'd like to describe. Must be an ID for deleted stacks
    :return: a list of all stack summaries (or, if a stack_name was specified and not found, None)
    """
    client = region.get_cloudformation()
    stacks_remain = True
    all_stacks = []
    token = None
    try:
        while stacks_remain:
            if token and stack_name:
                stacks = client.describe_stacks(StackName=stack_name, NextToken=token)
            elif stack_name:
                stacks = client.describe_stacks(StackName=stack_name)
            elif token:
                stacks = client.describe_stacks(NextToken=token)
            else:
                stacks = client.describe_stacks()
            all_stacks.extend(stacks['Stacks'])
            if 'NextToken' in stacks:
                token = stacks['NextToken']
            stacks_remain = 'NextToken' in stacks
    except ClientError:  # if the stack_name provided isn't found
        return []
    return all_stacks


def find_stacks(match_all = True, **tags):
    """
    Find stacks that match the given tags.

    Example usage::

        # find stacks where the tag named 'VpcName' equals 'cicd'
        result = find_stacks(VpcName='cicd')

    :param tags: Keyword arguments representing the tags to match. Tags with value `None` will simply be ignored.
    :param match_all: If enabled, only stacks which match *all* the given tags will be returned. If disabled, will return stacks with *any* matches. Enabled by default.
    :return: A list of matching stacks
    """
    tags = { key: value for key, value in tags.items() if value is not None }

    def has_tag(stack, tag):
        'Return whether the stack has the given tag'
        key, value = tag
        return any(stack_tag.get('Key') == key and stack_tag.get('Value') == value for stack_tag in stack['Tags'])

    def matches(stack):
        'Return whether the stack is a match'
        tags_found = [ has_tag(stack, tag) for tag in tags.items() ]
        return match_all and all(tags_found) or not match_all and any(tags_found)

    return list(filter(matches, describe_stacks()))


def find_stack(match_all = True, **tags):
    """
    Find the first stack that matches the given tags. Usage is the same as `find_stacks()`.

    :param tags: Keyword arguments representing the tags to match
    :param match_all: If enabled, only a stack which match *all* the given tags will be returned. If disabled, will return a stack with *any* matches. Enabled by default.
    :return: The first matching stack
    """
    matching_stacks = find_stacks(match_all=match_all, **tags)
    return matching_stacks[0] if matching_stacks else None


def get_stack_status(stack_name: str):
    """
    Extracts just the StackStatus field.  This is useful for
    waiting on the stack for a status change.

    :param stack_name: Stack to query.
    :return: string value of status or None if the stack wasn't found
    """
    stacks = describe_stacks(stack_name=stack_name)
    if stacks:
        return stacks[0]['StackStatus']
    return None  # changed from a string status


def get_stack(stack_name: str):
    """
    Gets the stack information.

    :param stack_name: Stack to query.
    :return: `cloudformation.Stack <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stack>`_
    """
    stacks = describe_stacks(stack_name)
    if stacks:
        return stacks[0]
    return None


def stack_exists(stack_name: str):
    """
    Returns true if StackStatus == CREATE_COMPLETE
    :param stack_name: Name of stack
    :return: True if StackStatus is CREATE_COMPLETE
    """
    # stacks = list_stacks(stack_status_filter = ['CREATE_COMPLETE', 'CREATE_IN_PROGRESS'])
    if describe_stacks(stack_name=stack_name):
        return True
    return False


def wait_for_stack(stack_name: str, pend_status: str):
    """
    Waits for the specified pend_status to clear.   This function
    will provide a spinner while waiting for the status to change.

    :param stack_name: Name of stack to observe.
    :param pend_status: Status we will wait on until it changes. For example, if the pend_status == CREATE_IN_PROGRESS, we'll wait until
                        it changes to something else like CREATE_COMPLETED.

    :return:
    """
    spinner = itertools.cycle('-\\|/')

    status = pend_status
    print(status)
    while status == pend_status:
        sys.stdout.write(spinner.__next__())  # write the next character
        sys.stdout.flush()  # flush stdout buffer (actual character display)
        sys.stdout.write('\b')
        time.sleep(1)
        status = get_stack_status(stack_name)

    print(status)
    return status


def create_stack(fn: str, params={}, capabilities=[], stack_name: str = None, tags: dict = {}, debug = False):
    """
    Creates a cloud formation stack.  The template file is preprocesssed with Jinja using
    the passed in parameters. If creation fails, the stack will be deleted,
    and an exception will be raised.

    :param fn: File name of cloud formation template
    :param params: Parameters required by the template
    :param capabilities: Used to add IAM capabilities if we are doing something that is powerful such as creating roles.
    :param stack_name: Used to specify a non-standard stack name
    :param tags: Dict of tags to be applied to the stack. Keys are the tag names; values are the tag values.
    :param debug: If set to True, outputs the template after Jinja template rendering.  Default is False.
    :return: `cloudformation.Stack <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stack>`_
    """
    client = region.get_cloudformation()

    try:
        # create stack name
        (path, filename) = os.path.split(fn)
        if stack_name is None:
            stack_name = params['VpcName'] + '-' + filename.split('.')[0]

        # if stack already exists, skip and return true
        if stack_exists(stack_name):
            print(f"{stack_name} already exists - skipping stack creation.")
            return get_stack(stack_name)

        print(f"Creating {stack_name}...")

        # Render Template
        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(filename)

        template_body = template.render(params)

        if debug:
            print(template_body)


        # get params list
        template_validated = client.validate_template(TemplateBody=template_body)

        # create parameters
        if template_validated.get('Parameters') is not None:
            cfn_params = [
                {'ParameterKey': kvp['ParameterKey'], 'ParameterValue': params[kvp['ParameterKey']]}
                for kvp in template_validated['Parameters']
            ]

        # parse tags
        tags_list = [{'Key': key, 'Value': value} for key, value in tags.items()]

        # create stack
        metadata = client.create_stack(StackName=stack_name,
                                   TemplateBody=template_body,
                                   Parameters=cfn_params,
                                   Capabilities=capabilities,
                                   OnFailure="DO_NOTHING",
                                   Tags=tags_list)

        # wait for the stack
        status = wait_for_stack(stack_name, CREATE_IN_PROGRESS)
        summary = get_stack(stack_name)
        po.print(summary)

        if status != CREATE_COMPLETE:
            delete_stack(stack_name)
            raise Exception(f'Stack creation failed: {stack_name}')

        return summary

    except IOError as e:
        print(f"Can't open stack {e}") 


def get_export_value(stack_name: str, export_name: str):
    """
    Gets a value that the given stack has exported

    :param stack_name: the name of the stack that exports the value
    :param export_name: the exported name (unique)
    :return: the exported value as a string
    """
    if not stack_exists(stack_name):
      return None
    outs = get_stack(stack_name)['Outputs']
    if not outs:
      return None
    for out in outs:
      if out['ExportName'] == export_name:
        return out['OutputValue']


def delete_stack(stack_name: str):
    """
    Deletes the specified stack.

    :param stack_name: Name of stack to remove
    :return: Last known status.
    """
    client = region.get_cloudformation()
    print(f'Deleting {stack_name}...')
    client.delete_stack(StackName=stack_name)
    status = wait_for_stack(stack_name, DELETE_IN_PROGRESS)

    return status


def get_output(stack, output_key: str):
    """
    Get output value from a given stack and output key. Either a stack dict or just the stack name can be provided.

    :param stack: Either a stack name or a stack dict.
    :param output_key: The output key to find
    """
    if type(stack) is str:
        stack_dict = get_stack(stack)
    elif type(stack) is dict:
        stack_dict = stack
    else:
        raise TypeError('Stack must be of type str or dict')

    if 'Outputs' not in stack_dict:
        raise ValueError('Invalid stack object: "Ouputs" property not found.')

    return next((o['OutputValue'] for o in stack_dict['Outputs'] if o.get('OutputKey') == output_key), None)


def get_resources(stack_name: str):
    """
    Get a list of stack resources

    :param stack_name: Name of stack
    :return: A list of resource details (`StackResource <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stackresource>`_)
    """
    if not stack_exists(stack_name):
        raise ValueError(f'Stack not found: {stack_name}')

    return region.get_cloudformation().describe_stack_resources(
        StackName=stack_name
    )['StackResources']


def get_resource(stack_name: str, logical_id: str):
    """
    Get a stack resource with the given logical id.

    :param stack_name: Name of stack
    :param logical_id: The logical id of the resource (its key in the CloudFormation template).
    :return: The resource details (`StackResource <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#stackresource>`_)
    """
    resources = get_resources(stack_name)
    match = ( resource for resource in resources if resource['LogicalResourceId'] == logical_id )
    return next(match, None)


def get_resource_id(stack_name: str, logical_id: str):
    """
    Get the physical id  of a stack resource with the given logical id.

    :param stack_name: Name of stack
    :param logical_id: The logical id of the resource (its key in the CloudFormation template).
    :return: The physical resource id (ARN, Name, etc.)
    """
    resource = get_resource(stack_name, logical_id)
    return resource['PhysicalResourceId'] if resource else None
