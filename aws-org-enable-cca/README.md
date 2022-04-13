<p align="center">
</p>

# Setup configuration compliance in an AWS Organization

## Overview

Demonstrates steps required to operationalize configuration compliance in AWS across an AWS Organization


## Step 1 - Enable Config in an AWS Organization 

**Option 1 - Use CloudFormation Stacksets** - In the CloudFormation console, choose StackSets. On the Create StackSets page, select the option to 'Use a sample template' and select the 'Enable AWS Config' template. Since you are using AWS Organizations [use service-managed permissions to deploy this template as a stackset]((https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html#stacksets-orgs-associate-stackset-with-org).)

**Option 2 - Use Systems Manager Quick Setup** - With [Quick Setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-quick-setup.html), a capability of AWS Systems Manager, you can quickly create a configuration recorder powered by AWS Config across your organization. Follow the [steps outlined in SSM Quick Setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/quick-setup-config.html) to set up AWS Config recording with AWS Systems Manager Quick Setup in an AWS Organization

## Step 2 - Register a delegated administrator account for AWS Config

From the **management account** of your AWS Organization, run the **register-delegated-administrator** command. In the following AWS CLI command, replace *delegated account id* with the delegated administrator account ID:

```
$ aws register-delegated-administrator --service-principal config.amazonaws.com\
--account-id [delegated account id]
```

## Step 3 - Setup S3 Delivery bucket in the delegated administrator account for Conformance Pack artifacts

For AWS Config to be able to store conformance pack artifacts, you will need to provide an Amazon S3 bucket in the **delegated administrator** account. This bucket name must start with the prefix **“awsconfigconforms”**. Each account in the organization must have access to this bucket. 

AWS Config recommends having limited permissions to the Amazon S3 bucket policy. To limit access, you can use following policy which uses **PrincipalOrgID** and **PrincipalArn** conditions in the Amazon S3 policy. This allows only accounts in an organization to have access to the bucket.  You can find your organization id from the AWS Organizations console under the Settings tab.

```
{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetPutObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                     "s3:GetObject",
                     "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::awsconfigconforms<suffix in bucket name>/*",
                "Condition": {
                    "StringEquals": {
                        "aws:PrincipalOrgID": "customer_org_id"
                    },
                    "ArnLike": {
                        "aws:PrincipalArn": "arn:aws:iam::*:role/aws-service-role/config-conforms.amazonaws.com/AWSServiceRoleForConfigConforms"
                    }
                }
            },
            {
                "Sid": "AllowGetBucketAcl",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetBucketAcl",
                "Resource": "arn:aws:s3:::awsconfigconforms<suffix in bucket name>",
                "Condition": {
                    "StringEquals": {
                        "aws:PrincipalOrgID": "customer_org_id"
                    },
                    "ArnLike": {
                        "aws:PrincipalArn": "arn:aws:iam::*:role/aws-service-role/config-conforms.amazonaws.com/AWSServiceRoleForConfigConforms"
                    }
                }
            }
        ]
}

```

