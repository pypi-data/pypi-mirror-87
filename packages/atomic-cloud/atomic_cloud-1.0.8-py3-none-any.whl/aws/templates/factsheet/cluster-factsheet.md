# Fact Sheet: {{VpcName}} cluster

This document provides a summary of the {{VpcName}} cluster and its associated resources.

## Basic Info

{% if accountAlias %}
**AWS Account:** [{{account}} ({{accountAlias}})](https://{{accountAlias}}.signin.aws.amazon.com/console)
{% else %}
**AWS Account:** [{{account}}](https://{{account}}.signin.aws.amazon.com/console)
{% endif %}

**Region:** {{region}}

## Resources

Relevant cluster resources, their identifiers, and links to the resources in the AWS Console.

### VPC
| Name | Description | CIDR Range | ID (Link) |
| ---- | ----------- | ---------- | ------------- |
| {{VpcName}}-vpc | Holds all resources for {{VpcName}} | {{cidrBase}}.0.0/16 | [{{vpcId}}](https://console.aws.amazon.com/vpc/home?region={{region}}#vpcs:VpcId={{vpcId}};sort=VpcId) |

### EKS Cluster
| Name | Description | ARN (Link) |
| ---- | ----------- | ---------- |
| {{cpName}} | Control plane | [{{cpArn}}](https://console.aws.amazon.com/eks/home?region={{region}}#/clusters/{{cpName}}) |
| {{ngName}} | Autoscaling group of worker nodes | [{{ngArn}}](https://console.aws.amazon.com/eks/home?region={{region}}#/clusters/{{cpName}}/nodegroups/standard-workers) |

### Subnets
| Type | Availability Zone | CIDR Range | ARN (Link) |
| ---- | ----------------- | ---------- | ---------- |
{% for az in azs %}
{% if loop.index0 != 1 and loop.index0 != 4 %}
| Private | {{az.ZoneName}} | {{cidrBase}}.{{loop.index0 + 100}}.0/24 | [{{subPrivateIds[loop.index0]}}](https://console.aws.amazon.com/vpc/home?region={{region}}#subnets:SubnetId={{subPrivateIds[loop.index0]}};sort=VpcId) |
{% endif %}
{% endfor %}
{% for az in azs %}
{% if loop.index0 != 1 and loop.index0 != 4 %}
| Public | {{az.ZoneName}} | {{cidrBase}}.{{loop.index0}}.0/24 | [{{subPublicIds[loop.index0]}}](https://console.aws.amazon.com/vpc/home?region={{region}}#subnets:SubnetId={{subPublicIds[loop.index0]}};sort=VpcId) |
{% endif %}
{% endfor %}

### Security Groups
| Name | Description | ID (Link) |
| ---- | ----------- | --------- |
| {{VpcName}}-02-cp-ControlPlaneSecurityGroup | Allow traffic for Master's rancher server | [{{sgMasterId}}](https://console.aws.amazon.com/ec2/v2/home?region={{region}}#SecurityGroups:group-id={{sgMasterId}}) |
| {{VpcName}}-02-cp-ClusterSharedNodeSecurityGroup | Allow internal traffic for k8s nodes | [{{sgNodesId}}](https://console.aws.amazon.com/ec2/v2/home?region={{region}}#SecurityGroups:group-id={{sgNodesId}}) |

### IAM Roles
| Name | Description | ARN (Link) |
| ---- | ----------- | ---------- |
| {{VpcName}}-cp-role | Control Plane Role | [{{cpRoleArn}}](https://console.aws.amazon.com/iam/home?{{region}}#/roles/{{VpcName}}-cp-role) |
| {{VpcName}}-nodes-role | Worker Nodes Role | [{{nodeRoleArn}}](https://console.aws.amazon.com/iam/home?{{region}}#/roles/{{VpcName}}-nodes-role) |

### RDS Instance
| Name | Description | Host | DB Identifier (Link) |
| ---- | ----------- | ---- | -------------------- |
| {{rdsName}} | RDS Instance (Postgres) | {{rdsHost}} | [{{rdsName}}](https://console.aws.amazon.com/rds/home?region={{region}}#database:id={{rdsName}};is-cluster=false) |