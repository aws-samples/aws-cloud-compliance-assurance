<p align="center">
</p>

# Automate change management in AWS with AWS Systems Manager Change Manager

Template 1 first provisions AWS Systems Manager Automation Documents as well as all the required pre-reqs. Template 2 then leverages the Systems Manager Automation documents within AWS Config Remediation Rules to incorporate change management in a remediation action via Systems Manager automation



## Solution Design

![](images/arch-changemanager.PNG)


## How To Install

1. **Template 1 of 2:** [aws-changemanager-ssmautomation.yml]()
* Provisions AWS Systems Manager automation documents. These documents are used to provide automated remediations within the provisioned AWS Config Rule.
* Provisions with fully built-in pre-reqs. No input parameters required. Simply install on the CloudFormation console (or CLI). Installs in approx 1-2 mins.

2. **Template 2 of 2:** [aws-changemanager-configremediation.yml]()
* Provisions AWS Config Managed Rules and attaches the custom AWS Systems Manager automation documents as AWS Config Remediations to the AWS Config Managed Rule. No input parameters. Simply install on the CloudFormation console (or CLI). Installs in approx 1-2 mins.
* Leverages the output from the previous template specifically the AWS Systems Manager Automation documents


