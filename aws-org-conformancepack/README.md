<p align="center">
</p>

# Deploy AWS Config Conformance Packs in an AWS Organization

## Pre-requisite
Deploying AWS Config Conformance Packs in an Organization requires the following pre-requisites: 

1. AWS Config recording is turned on in the management and member accounts in which you wish to deploy the organization conformance pack.
2. An Amazon S3 bucket is available in the management or member account for storing the conformance pack template with access granted to the organization.
	- The bucket name must start with the prefix “awsconfigconforms”. Each account in the organization must have access to this bucket.  
	- This bucket is the S3 delivery bucket that is required when deploying a conformance pack in an organization

## Deploy an AWS Config Conformance Pack in an AWS Organization - Sample Template

1. Launch the sample **OrgEnableConformancePack.yml** from the management account of your AWS Organization.
1. Modify this snippet for deploying other Conformance Packs.