<p align="center">
</p>

# Deploy custom AWS Config Conformance Packs in an AWS Organization


## 0 - Prerequsites
1. Complete the setup in [aws-org-enable-cca](https://github.com/aws-samples/aws-cloud-compliance-assurance/tree/main/aws-enable-config)


## 1 - Deploy custom Config Conformance Pack

1. Upload custom conformance pack template (aws-pci-conformancepack-v1.yml) in s3 (template-uri)
2. Use CloudFormation template (aws-pci-customconfpack-org.yml) for org wide deployment of custom conformance pack



## 2-  Deploy custom Config Conformance Pack with remediations in an AWS Organization

1.	Deploy  PCI SSM automation template (aws-pci-confpack-ssmautomation-v1.yml) org wide using Stacksets and service managed permissions
2.	Modify <accountid> parameter with the account id of the delegated administrator account in the custom conformance pack template with remediations (aws-pci-conformancepack-remediations-v1.yml) 
3.	Upload custom conformance pack template with remediations (aws-pci-conformancepack-remediations-v1.yml) in s3 (template-uri)
4.	Use CloudFormation template (aws-pci-customconfpack-org.yml) for org wide deployment of custom conformance pack with remediations
