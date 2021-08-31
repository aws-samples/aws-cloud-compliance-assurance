<p align="center">
</p>

# Prescriptive Compliance with Service Catalog and Config. Use a CCOE approach to standardize compliance

 This solution demonstrates the combined use of DevOps automation and Infrastructure as Code (IaC) via AWS CodePipeline, AWS Service Catalog and AWS CloudFormation to enable CCOE (Cloud Center of Excellence) AWS administrators and infrastructure engineers to automate the management and deployment of Service Catalog Portfolios that contain Service Catalog Products containing AWS Config rules and integrated AWS Systems Manager (SSM) remediation runbooks

 We will deploy this solution in a multi account organization.  Our organization deployed via AWS Organizations comprises of a Shared Services account which is where CCOE (Cloud Center of Excellence) administrators can deploy shared service and can add/remove/update compliance rules. These updates flow through a devops based AWS CodePipeline deployment to the managed accounts and result in updated compliance related Service Catalog Portfolios in the managed accounts. The entire solution is setup in 1 step with Infrastructure as Code (IaC) automation using AWS CloudFormation.


## Personas

1. CCOE AWS administrator
	1. The CCOE administrator performs initial setup from the shared services account. After setup, the DevOps infrastructure (AWS CodePipeline) is provisioned in the shared services account, and an AWS Service Catalog Portfolio with Config rules and integrated remediation runbooks is provisioned in the managed accounts.
	2. The CCOE administrator also performs code updates from the local Git repository. The administrator checks in updated Config rules and remediation runbook templates and (optionally) an updated buildspec.yaml file. The updated code flows via AWS CodePipeline in the AWS shared services account and updates the AWS Service Catalog Portfolio in the managed accounts.

2. End user / AWS administrator in the managed accounts
The end user launches the Config rules and integrated remediation runbooks from the AWS Service Catalog console in the managed account. 

## What is implemented

The following AWS CloudFormation templates have been implemented for this solution -
1. aws-servicecatalog-codepipeline.yaml – Sets up the AWS CodePipeline automation in the Shared Services account that distributes service catalog portfolios to the managed accounts
2. aws-servicecatalog-prescriptivecompliance.yml – Sets up the  AWS Service Catalog Portfolio that consists of  Service Catalog Products comprised of Config rules with remediation runbooks


## Architecture

![](images/ccoe-prescriptivecompliance.PNG)


## Pre-requisites

1. As a CCOE AWS administrator signed in to the AWS shared services account, set up the following resources.
Enable AWS Config in the shared service account and all your managed accounts in the organization. Perform step 1 from the Automate configuration compliance at scale blog post to use Systems Manager quick setup to do that with just a few clicks from your console.
2.	Integrate AWS Cloud9 local Git repository with AWS CodeCommit remote Git repository
	1. I have provided an aws-servicecatalog-configremediations-v1.yml AWS CloudFormation template that contains AWS Config Managed rules with integrated AWS Systems Manager remediation runbooks for common cloud configuration compliance violations. You can get the AWS CloudFormation template that provides a full coverage of PCI rules with SSM remediation runbooks from this PCI and FSBP Config Rules with SSM remediations repository
	2. Create an AWS CodeCommit Git repository in the shared services account and integrate it with your local Git repository.  Using AWS Cloud9 is one of the easiest ways in AWS to set up a local Git repository and integrate with CodeCommit as the remote Git repository. Follow these steps to setup Cloud9 and integrate with a CodeCommit repository.  
3.	Download these files from this solution’s GitHub repo and upload them to your Cloud9 local Git repository. My local Cloud9 Git repository contains the following files in this structure.
	1. Compliance product templates:
		1. aws-servicecatalog-configremediations-v1.yml in a compliance folder
		2. aws-servicecatalog-prescriptivecompliance.yml in the root folder
	2. buildspec.yml in the root folder
	3. buildspec-update.yml in the root folder
4.	Create an S3 staging bucket using this naming convention: s3-configremediations-*accountid*-*region*. Create a folder called ‘compliance’in your S3 bucket. The folder names here need to match the folder names in your local Git repository. You can create these folders with any names as long as those are the same names used while creating your local Git repository there.
5.	In the following files that are available for download from the solution, substitute the *accountid* parameter with the AWS Account ID of the shared services account. Substitute the *region* parameter with the AWS region of your shared services account. Substitute the *managedaccount* and *managedregion* parameters with comma separated AWS Account IDs and comma separated AWS regions respectively of the managed accounts where the solution will be deployed.
	1. buildspec.yml
	2. buildspec-updates.yml


## How to Install and Test

The initial set up is done in 1 step by the CCOE (Cloud Center of Excellence) AWS Administrator from the shared services account.

1. Launch the aws-servicecatalog-codepipeline.yml template. The template takes the following parameters and you can accept all defaults.
	1. RepositoryName: CodeCommit repository for the Config remediation CloudFormation templates
	2. BranchName: Branch in the CodeCommit repository for the Config Remediation CloudFormation templates
	3. S3StagingBucketPrefix: Prefix for the S3 Staging Bucket that stages the code copied from code commit.  In our case this is s3-configremediations-*accountid*-*region*
 
This 1 step executes the following -
1. The template provisions AWS CodePipeline in the AWS Shared Services account.
2. The AWS CodeCommit stage of AWS CodePipeline downloads the code from the AWS CodeCommit Git repository and into the Amazon S3 artifact repository of AWS CodePipeline.
3. The AWS CodeBuild stage of AWS CodePipeline uses the AWS Service Catalog Portfolio template, executes the commands in the buildspec.yaml file to stage the code in an S3 bucket, and leverages AWS CloudFormation StackSets to launch the aws-configremediations-servicecatalog-portfolio in the managed accounts. 
	1. This last step creates the AWS Service Catalog Portfolio in the managed accounts with the Config rules and integrated remediation runbooks Service Catalog Products. 
	2. This step also creates an end user group (EndUserGroup), an end user role (EndUserRole) and a launch constraint in the managed accounts. This allows an IAM end user in the managed accounts to log in and directly use the AWS Service Catalog console to launch the Config rules with remediation runbooks products. 



In order to test that the initial setup was successful, login to the Managed Account as an end	user and perform the following step–

1.	Log in to the managed account as an end user.
2.	Navigate to the Service Catalog console in the AWS managed account and click on Products in the left panel of the console.  Select a product and launch Trend Micro products and the Trend Micro Deep Security agent directly from here. As a best practice, the AWS Service Catalog product for the Trend Micro agent is set up to allow deployment of Trend Micro Deep Security agents to EC2 instances based on resource tags.
3.	Accept the defaults to test the launch of the Trend Micro Deep Security agent.
4.	Follow the instructions in the Deep Security Quick Start to set up Trend Micro Deep Security.


Updates are performed directly from the local GitHub repository. The CCOE AWS Administrator checks in updated TrendMicro source template(s) in this step. If this is the first time that this update is being performed, then the check-in should also include a modified buildspec.yml file. Replace the existing buildspec.yaml with the buildspec-updates.yml file and rename the buildspec-updates.yml to buildspec.yml. The modified buildspec.yaml file invokes update-stackset on CloudFormation instead of a create-stackset. 


AWS CodePipeline will automatically recognize the commit and proceed through its stages and actions and update the Trend Micro products in AWS Service Catalog of the managed accounts. The automated pipeline for managing AWS Service Catalog is now set up and responding to template changes via git commits.

For our walkthrough, let’s test performing updates as a CCOE administrator.

1.	In your local git repository and inside the distributor agent folder, rename the aws-systemsmanagerdistributor-agent-v1.yaml file to aws-systemsmanagerdistributor-agent-v2.yaml. Assume that you have a new version of the agent and a new version of this template has been created for that and checked in your source code repository.
2.	In your local git repository, update the aws-trendmicro-servicecatalog-portfolio AWS CloudFormation template. Look for the Resources section in this template and specifically the TrendMicroDeepSecurityAgent Resource. Update the ProvisioningArtifactParameters section with the following: 
	Description: This is version 2.0 of Trend Micro Deep Security Agent
	Name: Version - 2.0
	Info: LoadTemplateFromURL: !Sub "${S3StagingBucketURL}distributoragent/aws-systemsmanagerdistributor-agent_v2.yaml"
3.	Replace the existing buildspec.yml file with buildspec-updates.yml. Rename buildspec-updates.yml to buildspec.yml.
4.	In your git bash terminal on your local machine, issue the following commands to update the AWS CodeCommit Repository with changes from your local git repository
	git add .
	git commit –m “version update”
	git push origin master
5.	Sign in to the AWS Shared Services account and open the AWS CodePipeline console. You should see that the code pipeline gets triggered due to a new commit in the AWS CodeCommit repository.
6.	Verify that all stages of the AWS CodePipeline complete successfully.
7.	Open the AWS CloudFormation console and choose StackSets and then Operations.
8.	Verify that the aws-trendmicro-servicecatalog-portfolio StackSet is updated successfully
9.	Sign in to the AWS managed account as an end user and open the AWS Service Catalog console.
10.	Verify that the Trend Micro Deep Security Agent product has been updated with the new version, template, and description.

