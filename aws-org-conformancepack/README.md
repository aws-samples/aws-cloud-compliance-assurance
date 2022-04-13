<p align="center">
</p>

# Deploy custom AWS Config Conformance Packs in an AWS Organization


## 0 - Prerequsites
1.	Ensure AWS Config  is enabled in each account
2.	Ensure an IAM role (service linked role) is provisioned in each account
3.	Ensure that there is s3 bucket that allows read/write from the IAM role in each account
4.	Recommended – Register delegated administrator account


## 1 - Deploy custom Config Conformance Pack

1. Launch the sample 'OrgEnableConformancePack.yml' template from the management account of your AWS Organization. The template takes the 'TemplateS3Uri' as a parameter which is the S3 template URI that hosts the conformance pack template. You can upload the sample 'org-confpack-pci'  conformance pack template to S3 and test an organizational deployment of that conformance pack.  Upload other conformance pack templates to S3 and use this template as a sample to deploy organization conformance packs.


## 2-  Deploy custom Config Conformance Pack with remediations in an AWS Organization

1. Deploy Stackset pre-requisites to enable self service permissions - Launch the AWSCloudFormationStackSetAdministrationRole.yaml template in the account where the stackset will be provisioned. Launch the AWSCloudFormationStackSetExecutionRole.yaml in each of the accounts where stack instances based on the stackset will be provisioned

2. In the CloudFormation console of the account where the AWSCloudFormationStackSetAdministrationRole.yaml was provisioned , choose StackSets. On the Create StackSets page, select the option to 'Upload a template file' and select the 'org-confpack-pci' sample conformance pack template. Select 'self service permissions' and provide the names of the AWSCloudFormationStackSetAdministration rol sample and  AWSCloudFormationStackSetExecution role. Modify this snippet for deploying other conformance Pack templates.