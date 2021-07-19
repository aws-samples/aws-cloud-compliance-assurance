<p align="center">
</p>

# Enable AWS Config Aggregator across accounts and regions

1. An AWS Config Aggregator is an AWS Config resource type that collects AWS Config configuration and compliance data from multiple accounts and regions or from an AWS organization. All accounts must have AWS Config enabled. 
2. The AWS account where the AWS Config Aggregator is created is called the aggregator account. The AWS account(s) that provide configuration and compliance data to this aggregator account are called the source accounts.
3. The aggregator account can be either the management account or a registered delegated administrator account. All features must be enabled in your organization.
	- If you are using a delegated administrator account as the aggregator account then ensure that the management account registers this account as the delegated administrator for the AWS Config service principle name (config.amazonaws.com).
4. If the Config Aggregator is configured to collect data from individual source accounts then each source account must provide authorization for the data to be collected. If the Config Aggregator is configured to collect data from an AWS organization then explicit authorization from a source account is not required.


## Option 1: Use OrganizationEnableRecorderAndAggregator.yaml - Create Config Aggregator in aggregator account for data collection across the AWS Organizaiton

1. Enables AWS Config in your account if Config is not already enabled. Provisions recorder, delivery channel, S3 bucket and bucket policy required to enable Config
2. Launch this template from the aggregator account. Creates an AWS Config Aggregator from the aggregator account. It uses a service linked role that retrieves AWS Organization details associated with the aggregator account.
	- This creates an IAM role that attaches the AWSConfigRoleForOrganizations managed policy to your IAM role. Attaching this policy allows AWS Config obtain Organization details associated with the aggregator account.


## Option 2: Use AccountEnableRecorderAndAggregator-v1.yaml - Create Config Aggregator in aggregator account and add authorization in individual source region(s) of that same account

1. Enables AWS Config in your account if Config is not already enabled. Provisions recorder, delivery channel, S3 bucket and bucket policy required to enable Config
2. Launch this template from the aggregator account. Provide input for the following parameters:
	*AggregatorAccount*: AWS Account ID of the aggregator account
	*AggregatorRegion*: AWS region of the aggregator
	*SourceRegion1:* AWS region to aggregate
	*SourceRegion2:* AWS region to aggregate













