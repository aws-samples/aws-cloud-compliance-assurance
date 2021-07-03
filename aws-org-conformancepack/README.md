<p align="center">
</p>

# Deploy AWS Config Conformance Packs across accounts and regions


## Option 1 - Deploy an AWS Config Conformance Pack in an AWS Organization - Sample

1. Launch the sample 'OrgEnableConformancePack.yml' template from the management account of your AWS Organization. Modify this snippet for deploying other Conformance Packs.


## Option 2: Deploy an AWS Config Conformance Pack in multiple accounts or regions ( not using AWS Organizations) - Sample

1. Deploy Stackset pre-requisites to enable self service permissions - Launch the AWSCloudFormationStackSetAdministrationRole.yaml template in the account where the stackset will be provisioned. Launch the AWSCloudFormationStackSetExecutionRole.yaml in each of the accounts where stack instances based on the stackset will be provisioned

2. In the CloudFormation console of the account where the AWSCloudFormationStackSetAdministrationRole.yaml was provisioned , choose StackSets. On the Create StackSets page, select the option to 'Upload a template file' and select the 'AccountEnableConformancePack.yml' template. Select 'self service permissions' and provide the names of the AWSCloudFormationStackSetAdministration role and  AWSCloudFormationStackSetExecution role. Modify this snippet for deploying other Conformance Packs