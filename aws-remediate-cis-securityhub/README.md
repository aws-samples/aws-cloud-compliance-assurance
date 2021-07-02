<p align="center">
</p>

# Automated Remediations for CIS Benchmarks using AWS Security Hub

The solution implemented here leverages the AWS Security Hub service and provides customers with an AWS native implementation for automated remediations for these CIS violations detected by AWS Security Hub.


## How it Works

This implementation is based on the following solution approach:

1. Leverages AWS Security Hub directly to provide continuous detection of CIS findings
2. Provides AWS Systems Manager Automation Documents for automated remediation for AWS Security Hub findings. All documents are automatically provisioned via an AWS CloudFormation template.
3. Provides integration of AWS Security Hub Custom Actions with AWS Systems Manager Automation Documents to provide real time remediations of AWS Security Hub FSBP findings as follows:
* Leverages the ability of AWS Security Hub to send findings associated with custom actions to CloudWatch Events as Security Hub Findings - Custom Action events.
* The CloudWatch Events Rule invokes the corresponding Lambda Function as the Target for the source Security Hub Custom Action event
* The Lambda function processes the finding using the standard findings format provided by Security Hub - AWS Security Finding Format (ASFF) and invokes the corresponding AWS Systems Manager Automation Document with the input from the ASFF finding


## Solution Design

![](images/arch-diagram.png)

## How To Install

1. **Template 1 of 3:** aws-aws-cis-cloudwatchlogmetricfilters.yml
* Provisions CloudWatch Logs Metric Filters. Enter email address as input. Simply install on the CloudFormation console (or CLI). Installs in approx 1-2 mins.

2. **Template 2 of 3:** aws-cis-systemsmanagerautomations.yml
* Provisions AWS Systems Manager automation documents. These documents are used to provide automated remediations within the provisioned AWS Security Hub Action.
* Provisions with fully built-in pre-reqs. No input parameters required. Simply install on the CloudFormation console (or CLI). Installs in approx 3-4 mins.

2. **Template 3 of 3:** aws-cis-securityhubactions.yml
* Provisions AWS CloudWatch Evemts and AWS Security Hub Custom Actions. No input parameters. Simply install on the CloudFormation console (or CLI). Installs in approx 3-4 mins.
* Leverages the output from the previous template specifically the AWS Systems Manager Automation documents





