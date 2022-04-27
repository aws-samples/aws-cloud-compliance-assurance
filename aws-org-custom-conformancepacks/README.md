<p align="center">
</p>

# Automate Cloud Foundations for Compliance in AWS



## Overview

1. Automated deployment of a custom AWS Config Conformance Pack in an AWS Organization. 
2. Automated deployment of AWS Systems Manager remediation runbooks in an AWS Organization. 
3. Add code for SSM remediations to a custom AWS Config Conformance Pack
4. Automated deployment of a custom AWS Config Conformance Pack with remediations in an AWS Organization. 

Demonstrates deployment of a custom Config conformance pack with remediations for these PCI controls:

```
* [PCI.AutoScaling.1] Auto scaling groups associated with a load balancer should use health checks
* [PCI.CloudTrail.3] CloudTrail log file validation should be enabled
* [PCI.CloudTrail.4] CloudTrail trails should be integrated with CloudWatch Logs
* [PCI.CodeBuild.2] CodeBuild project environment variables should not contain clear text credentials
* [PCI.EC2.2] VPC default security group should prohibit inbound and outbound traffic
* [PCI.EC2.3] Unused EC2 security groups should be removed
* [PCI.EC2.4] Unused EC2 EIPs should be removed
* [PCI EC2.5] Security groups should not allow ingress from 0.0.0.0/0 to port 22 
* [PCI.IAM.3] IAM policies should not allow full * administrative privileges
* [PCI.KMS.1] Customer master key (CMK) rotation should be enabled
* [PCI.Lambda.1] Lambda functions should prohibit public access
* [PCI.RDS.1] RDS snapshots should prohibit public access
* [PCI.RDS.2] RDS DB Instances should prohibit public access
* [PCI.Redshift.1] Amazon Redshift clusters should prohibit public access
* [PCI.S3.1] S3 buckets should prohibit public write access
* [PCI.S3.2] S3 buckets should prohibit public read access
```


## 0 - Prerequsites
1. Complete the setup in [aws-org-enable-cca](https://github.com/aws-samples/aws-cloud-compliance-assurance/tree/main/aws-org-enable-cca)


## 1 - Deploy custom Config Conformance Pack in an AWS Organization

1. In your **delegated administrator** account, create an S3 bucket. Upload the [**aws-pci-conformancepack-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-v1.yml) custom conformance pack template that you want to deploy in your AWS Organization. You will use the S3 URI that contains this template as the TemplateS3Uri parameter in the next step.
2. Launch the [**aws-pci-customconfpack-org.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-custom-confpack-org.yml) template from your **delegated administrator** account. This template automates org wide deployment of custom conformance packs. Provide the following parameters:
	- **DeliveryS3Bucket**: The name of the Amazon S3 bucket where AWS Config stores artifacts for org wide deployment of conformance pack templates. Obtain this value from the Org Conformance Pack pre-requisites that you completed.
	- **OrganizationConformancePackName**: Name of the custom config conformance pack
	- **TemplateS3Uri**: S3 URI that points to the location in S3 of the custom conformance pack template that you want to deploy in your AWS Organization. 

## 2-  Deploy custom Config Conformance Pack with remediations in an AWS Organization

1.	From your **management account**, launch the [**aws-pci-confpack-ssmautomation-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-confpack-ssmautomation-v1.yml) as a CloudFormation stackset. [Use service-managed permissions to deploy this template automatically throughout your AWS Organization using CloudFormation stacksets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html#stacksets-orgs-associate-stackset-with-org). 
2. Replace the **accountID** used for all the **AutomationAssumeRole** parameters within the [**aws-pci-conformancepack-remediations-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-remediations-v1.yml) custom Config Conformance Pack with SSM remediations template with the AWS AccountID of your **delegated administrator** account.
3. Upload the modified [**aws-pci-conformancepack-remediations-v1.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-conformancepack-remediations-v1.yml) custom Config Conformance Pack with SSM remediations template to an S3 bucket in your **delegated administrator** account. You will use the S3 URI that contains this template as the TemplateS3Uri parameter in the next step.
4. Launch the [**aws-pci-customconfpack-org.yml**](https://github.com/aws-samples/aws-cloud-compliance-assurance/blob/main/aws-org-custom-conformancepacks/cft/aws-pci-custom-confpack-org.yml) template from your **delegated administrator** account. This template automates org wide deployment of custom conformance packs. Provide the following parameters:
	- **DeliveryS3Bucket**: The name of the Amazon S3 bucket where AWS Config stores artifacts for org wide deployment of conformance pack templates. Obtain this value from the Org Conformance Pack pre-requisites that you completed.
	- **OrganizationConformancePackName**: Name of the custom config conformance pack with remediations
	- **TemplateS3Uri**: S3 URI that points to the location in S3 of the custom conformance pack template with remediations that you want to deploy in your AWS Organization. 


