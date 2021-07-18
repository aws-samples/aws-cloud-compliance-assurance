<p align="center">
</p>

# Deploy AWS Config Conformance Packs across accounts and regions


## Option 1 - Deploy an AWS Config Conformance Pack in an AWS Organization - Sample

1. Launch the sample 'OrgEnableConformancePack.yml' template from the management account of your AWS Organization. The template takes the 'TemplateS3Uri' as a parameter which is the S3 template URI that hosts the conformance pack template. You can upload the sample 'org-confpack-pci'  conformance pack template to S3 and test an organizational deployment of that conformance pack.  Upload other conformance pack templates to S3 and use this template as a sample to deploy organization conformance packs.


## Option 2: Deploy an AWS Config Conformance Pack in multiple accounts or regions ( not using AWS Organizations) - Sample

1. Deploy Stackset pre-requisites to enable self service permissions - Launch the AWSCloudFormationStackSetAdministrationRole.yaml template in the account where the stackset will be provisioned. Launch the AWSCloudFormationStackSetExecutionRole.yaml in each of the accounts where stack instances based on the stackset will be provisioned

2. In the CloudFormation console of the account where the AWSCloudFormationStackSetAdministrationRole.yaml was provisioned , choose StackSets. On the Create StackSets page, select the option to 'Upload a template file' and select the 'AccountEnableConformancePack.yml' template. Select 'self service permissions' and provide the names of the AWSCloudFormationStackSetAdministration role and  AWSCloudFormationStackSetExecution role. Modify this snippet for deploying other Conformance Packs