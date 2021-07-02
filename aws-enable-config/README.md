<p align="center">
</p>

# Enable Config and Config Rules in an AWS Organization

## Enable Config in an AWS Organization
AWS CloudFormation StackSets helps enable AWS Config on all member accounts under organizational units in a single execution. 

1. In the CloudFormation console, choose StackSets.
2. On the Create StackSets page, upload a template file
3. For choosing a template file, select the Enable AWS Config template
4. *Pre-requisite* - The administrator account must have an AWSCloudFormationStackSetsAdministrationRole IAM role and the target member accounts must have a corresponding AWSCloudFormationStackSetsExecutionRole. Refer to the guidance here:https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html#stacksets-prereqs-accountsetup

## Enable Managed Config Rules in an AWS Organization - Sample Template

1. Launch the sample **OrgEnableConfigRule.yml** from the management account of your AWS Organization.
1. Modify this snippet for deploying other Config managed rules