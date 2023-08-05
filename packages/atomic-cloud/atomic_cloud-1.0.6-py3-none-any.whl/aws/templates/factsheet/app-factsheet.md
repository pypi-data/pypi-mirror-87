# Application Fact Sheet: {{app_name}}

This document provides a summary of **{{app_name}}** and its associated resources in each environment.

## Basic Info

{% if account_alias %}
**AWS Account:** [{{account}} ({{account_alias}})](https://{{account_alias}}.signin.aws.amazon.com/console)
{% else %}
**AWS Account:** [{{account}}](https://{{account}}.signin.aws.amazon.com/console)
{% endif %}

**Region:** {{region}}

## Resources

Relevant application resources, their identifiers, and links to the resources in the AWS Console, grouped by environment.

{% for vpc_name in resources_by_vpc %}
{% set s3_storage_bucket, s3_host_bucket, cf_dist = resources_by_vpc[vpc_name] %}
### {{vpc_name}}

| Type | Description | ID (Link) |
| ---- | ----------- | --------- |
| ECR Repository | Image repository for this application | [{{ecr_repo}}](https://console.aws.amazon.com/ecr/repositories/{{ecr_repo}}/?region={{region}}) |
| S3 Storage Bucket | Bucket for backend storage | [{{s3_storage_bucket}}](https://s3.console.aws.amazon.com/s3/buckets/{{s3_storage_bucket}}/)
| S3 Host Bucket | Bucket for hosting the static frontend | [{{s3_host_bucket}}](https://s3.console.aws.amazon.com/s3/buckets/{{s3_host_bucket}}/) |
| Cloudfront Distribution | Provides HTTPS access to the frontend | [{{cf_dist}}](https://console.aws.amazon.com/cloudfront/home?region={{region}}#distribution-settings:{{cf_dist}})

{% endfor %}