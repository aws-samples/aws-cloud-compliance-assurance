<p align="center">
</p>

# Deploy custom AWS Config Conformance Packs in an AWS Organization


## Overview

1. Demonstrates automated deployment of a custom AWS Config Conformance Pack to an AWS Organization. 
2. Demonstrates automated deployment of AWS Systems Manager remediation runbooks to an AWS Organization. 
3. Demonstrates adding SSM remediations to a custom AWS Config Conformance Pack
4. Demonstrates automated deployment of a custom AWS Config Conformance Pack with remediations to an AWS Organization. 

Deploys a custom Config conformance pack with remediations for these PCI controls:
* [PCI.AutoScaling.1] Auto scaling groups associated with a load balancer should use health checks
* [PCI.CloudTrail.1] CloudTrail logs should be encrypted at rest using AWS KMS CMK
* [PCI.CloudTrail.2] CloudTrail should be enabled
* [PCI.CloudTrail.3] CloudTrail log file validation should be enabled
* [PCI.CloudTrail.4] CloudTrail trails should be integrated with CloudWatch Logs
* [PCI.CodeBuild.2] CodeBuild project environment variables should not contain clear text credentials
* [PCI.CW.1] A log metric filter and alarm should exist for usage of the "root" user
* [PCI.Config.1] AWS Config should be enabled
* [PCI.EC2.1] Amazon EBS snapshots should not be publicly restorable
* [PCI.EC2.2] VPC default security group should prohibit inbound and outbound traffic
* [PCI.EC2.3] Unused EC2 security groups should be removed
* [PCI.EC2.4] Unused EC2 EIPs should be removed
* [PCI EC2.5] Security groups should not allow ingress from 0.0.0.0/0 to port 22 
* [PCI.EC2.6] Ensure VPC flow logging is enabled in all VPCs
* [PCI.IAM.1] IAM root user access key should not exist
* [PCI.IAM.2] IAM users should not have IAM policies attached
* [PCI.IAM.3] IAM policies should not allow full * administrative privileges
* [PCI.KMS.1] Customer master key (CMK) rotation should be enabled
* [PCI.Lambda.1] Lambda functions should prohibit public access
* [PCI.Lambda.2] Lambda functions should be in a VPC
* [PCI.RDS.1] RDS snapshots should prohibit public access
* [PCI.RDS.2] RDS DB Instances should prohibit public access
* [PCI.Redshift.1] Amazon Redshift clusters should prohibit public access
* [PCI.S3.1] S3 buckets should prohibit public write access
* [PCI.S3.2] S3 buckets should prohibit public read access
* [PCI.S3.3] S3 buckets should have cross-region replication enabled
* [PCI.S3.4] S3 buckets should have server-side encryption enabled
* [PCI.SSM.1] Amazon EC2 instances managed by Systems Manager should have a patch compliance status of COMPLIANT after a patch installation

## 0 - Prerequsites
1. Complete the setup in [aws-org-enable-cca](https://github.com/aws-samples/aws-cloud-compliance-assurance/tree/main/aws-enable-config)


## 1 - Deploy custom Config Conformance Pack

1. In your delegated administrator account, create an S3 bucket. Upload the [**aws-pci-conformancepack-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-v1.yml) custom conformance pack template that you want to deploy in your AWS Organization. You will use the S3 URI that contains this template as the TemplateS3Uri parameter in the next step.
2. Launch the [**aws-pci-customconfpack-org.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-custom-confpack-org.yml) template from your delegated administrator account. This template automates org wide deployment of custom conformance packs. Provide the following parameters:
	- **DeliveryS3Bucket**: The name of the Amazon S3 bucket where AWS Config stores artifacts for org wide deployment of conformance pack templates. Obtain this value from the Org Conformance Pack pre-requisites that you completed.
	- **OrganizationConformancePackName**: Name of the custom config conformance pack
	- **TemplateS3Uri**: S3 URI that points to the location in S3 of the custom conformance pack template that you want to deploy in your AWS Organization. 

## 2-  Deploy custom Config Conformance Pack with remediations in an AWS Organization

1.	From your *management account*, launch the [**aws-pci-confpack-ssmautomation-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-confpack-ssmautomation-v1.yml) as a CloudFormation stackset. (Use service-managed permissions to deploy this template automatically throughout your AWS Organization using CloudFormation stacksets) [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html#stacksets-orgs-associate-stackset-with-org]. 
2. Replace the **accountID** used for all the **AutomationAssumeRole** parameters within the [**aws-pci-conformancepack-remediations-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-remediations-v1.yml) custom Config Conformance Pack with SSM remediations template with the AWS AccountID of your *delegated administrator* account.
3. Upload the modified [**aws-pci-conformancepack-remediations-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-remediations-v1.yml) custom Config Conformance Pack with SSM remediations template to an S3 bucket in your *delegated administrator* account. You will use the S3 URI that contains this template as the TemplateS3Uri parameter in the next step.
4. Launch the [**aws-pci-customconfpack-org.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-custom-confpack-org.yml) template from your delegated administrator account. This template automates org wide deployment of custom conformance packs. Provide the following parameters:
	- **DeliveryS3Bucket**: The name of the Amazon S3 bucket where AWS Config stores artifacts for org wide deployment of conformance pack templates. Obtain this value from the Org Conformance Pack pre-requisites that you completed.
	- **OrganizationConformancePackName**: Name of the custom config conformance pack with remediations
	- **TemplateS3Uri**: S3 URI that points to the location in S3 of the custom conformance pack template with remediations that you want to deploy in your AWS Organization. 


