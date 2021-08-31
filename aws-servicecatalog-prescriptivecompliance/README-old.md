<p align="center">
</p>

# Prescriptive Compliance with Service Catalog and Config

Standardize the provisioning and set up of configuration compliance using AWS Service Catalog and AWS Config Rules with custom Config Remediations


## Install

1. Launch the sample 'aws-servicecatalog-prescriptivecompliance.yml' template from any account in your organization where Config is already enabled.
2. Provisions a AWS Service Catalog Portfolio with an AWS Config Remediations Product.
   - The AWS Config Remediations Product provides automated detection with AWS Config and automated remediations with custom AWS Systems Manager documents
   - Provisions all pre-reqs for AWS Systems Manager Remediations
   - Provisions Custom AWS Systems Manager Automation Documents to provide Automated Remediations for AWS Config
   - For demo purposes (for GameDay, Reinforce etc) the template provisions misconfigured resources to trigger an attack and then also provisions on demand evaluations for AWS Config to detect and then remediate the attack with provisioned custom SSM remediations
   - Creates a launch constraint for a "Team Member' Role. In your AWS account, create a Team Member IAM role and add an IAM user to that role to demonstrate end user access to the catalog. Ignore this step if the AWS account is provisioned by Event Engine






