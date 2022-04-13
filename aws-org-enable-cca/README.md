<p align="center">
</p>

# Enable Config and Config Rules across accounts or regions

## Option 1: Enable Config in an AWS Organization 

1. In the CloudFormation console, choose StackSets. On the Create StackSets page, select the option to 'Use a sample template' and select the 'Enable AWS Config' template. Since you are using AWS Organizations use service managed permissions to deploy this template

## Option 2: Enable Config in multiple accounts or regions ( not using AWS Organizations)

1. Deploy Stackset pre-requisites to enable self service permissions - Launch the AWSCloudFormationStackSetAdministrationRole.yaml template in the account where the stackset will be provisioned. Launch the AWSCloudFormationStackSetExecutionRole.yaml in each of the accounts where stack instances based on the stackset will be provisioned

2. In the CloudFormation console of the account where the AWSCloudFormationStackSetAdministrationRole.yaml was provisioned , choose StackSets. On the Create StackSets page, select the option to 'Use a sample template' and select the 'Enable AWS Config' template. Select 'self service permissions' and provide the names of the AWSCloudFormationStackSetAdministration role and  AWSCloudFormationStackSetExecution role. 


# Enable Managed Config Rules

## Option 1: Enable Config Rule in an AWS Organization  - Sample

1. Launch the sample 'OrgEnableConfigRule.yml' template from the management account of your AWS Organization. Provide the AWS Config Managed Rule identifier as a parameter. Modify this snippet for deploying other Config managed rules

## Option 2: Enable Config Rule in multiple accounts or regions (not using AWS Organizations) - Sample

1. Deploy Stackset pre-requisites to enable self service permissions - Launch the AWSCloudFormationStackSetAdministrationRole.yaml template in the account where the stackset will be provisioned. Launch the AWSCloudFormationStackSetExecutionRole.yaml in each of the accounts where stack instances based on the stackset will be provisioned

2. In the CloudFormation console of the account where the AWSCloudFormationStackSetAdministrationRole.yaml was provisioned , choose StackSets. On the Create StackSets page, select the option to 'Use a sample template' and select the 'cloudtrail-enabled' template. Select 'self service permissions' and provide the names of the AWSCloudFormationStackSetAdministration role and  AWSCloudFormationStackSetExecution role. 