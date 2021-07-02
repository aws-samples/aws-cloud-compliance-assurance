
#  CreateAuditManagerAssessment-SecurityHub Lambda 
#  - Selects several AWS Security Hub checks as a data source
#  - Creates Custom Audit Manager Control Sets for IAM, API and Network Monitoring based on 
#    Security Hub checks across PCI,CIS and FSBP frameworks
#  - Creates an AWS Audit Manager custom framework with the control set above that uses Security Hub as a data source
#  - Creates an AWS Audit Manager assessment based on the custom framework above

# @kmmahaj
#
## License:
## This code is made available under the MIT-0 license. See the LICENSE file.


import json
import copy
import sys
import datetime
import boto3
import botocore
import time
import logging
import random
import urllib3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)
http = urllib3.PoolManager()

def cfnsend(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    
    responseUrl = ''
    StackId =''
    RequestId =''
    LogicalResourceId =''
    
    if 'ResponseURL' in event:
        responseUrl = event['ResponseURL']
    
    if 'StackId' in event:
        StackId = event['StackId']
    
    if 'RequestId' in event:
        RequestId = event['RequestId']
        
    if 'LogicalResourceId' in event:
        LogicalResourceId = event['LogicalResourceId']
        
    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : StackId,
        'RequestId' : RequestId,
        'LogicalResourceId' : LogicalResourceId,
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)


    except Exception as e:

        print("send(..) failed executing http.request(..):", e)


def create_custom_auditmanager_control(controls, controltype):
    
    auditmanager = boto3.client('auditmanager')
    securityhubcontrol_List= []
    control_id =""
    
    #Create a Custom Security Hub Control Source - Security Hub Control Source
    securityhub_controlmappingsource_template = {}
    securityhub_controlmappingsource_template['sourceName'] = 'Custom Security Hub Control Source'
    securityhub_controlmappingsource_template['sourceDescription'] = 'Security Hub checks'
    securityhub_controlmappingsource_template['sourceSetUpOption'] = 'System_Controls_Mapping'
    securityhub_controlmappingsource_template['sourceType'] = 'AWS_Security_Hub'
    sourceKeyword = {
                'keywordInputType': 'SELECT_FROM_LIST',
                'keywordValue': 'Security Hub checks'
            }
    securityhub_controlmappingsource_template['sourceKeyword'] = sourceKeyword
    
    for controlname in controls:
        securityhub_controlmappingsource = copy.deepcopy(securityhub_controlmappingsource_template)
        securityhub_controlmappingsource['sourceKeyword']['keywordValue'] = controlname
        securityhubcontrol_List.append(securityhub_controlmappingsource)
        
        
    #Create a Custom Security Hub Control
    name = 'Custom' + controltype + 'SecurityHubControl'
    response_control = auditmanager.create_control(name=name, controlMappingSources=securityhubcontrol_List)
    control_id = response_control['control']['id']
    
    return control_id
    

def lambda_handler(event, context):
   
    print ("boto3 version: " +  boto3.__version__)
    auditmanager = boto3.client('auditmanager')
    ssm = boto3.client('ssm')

    logger.info('EVENT Received: {}'.format(event))
    responseData = {}
    controlSets_List =[]

    #Handle cfnsend delete event
    eventType = event['RequestType']
    if eventType == 'Delete':
        logger.info(f'Request Type is Delete; unsupported')
        cfnsend(event, context, 'SUCCESS', responseData)
        return 'SUCCESS'
    
    #Create a Custom Security Hub IAM Audit Manager Control
    iam_controls = ['IAM.1', 'IAM.2', 'IAM.3', 'IAM.4', 'IAM.5', 'IAM.6', 'PCI.IAM.7', '1.16', '1.20', 'PCI.IAM.8']
    iam_controlid = create_custom_auditmanager_control(iam_controls,'IAM')
    
    #Create a Custom Security Hub IAM Control Set   
    sh_iam_controlset = {}
    sh_iam_controlset['name'] = 'Custom Security Hub IAM Control Set'
    sh_iam_controlset['controls'] = []
    iam_controldict ={}
    iam_controldict['id'] =  iam_controlid
    sh_iam_controlset['controls'].append(iam_controldict)
    controlSets_List.append(sh_iam_controlset)
 
    #Create a Custom Security Hub Montoring Audit Manager Control
    monitoring_controls = ['APIGateway.1', '2.9', '3.10', '3.11', '3.12', '3.13', '3.14', 'PCI.EC2.6']
    monitoring_controlid = create_custom_auditmanager_control(monitoring_controls, 'Monitoring')
    
    #Create a Custom Security Hub Monitoring Control Set   
    sh_mon_controlset = {}
    sh_mon_controlset['name'] = 'Custom Security Hub Monitoring Control Set'
    sh_mon_controlset['controls'] = []
    mon_controldict ={}
    mon_controldict['id'] =  monitoring_controlid
    sh_mon_controlset['controls'].append(mon_controldict)
    controlSets_List.append(sh_mon_controlset)

    #Create a Custom Security Hub Framework that contains 1) IAM Control Set and 2) Network Monitoring Control Set
    
    response_framework = auditmanager.create_assessment_framework(name='Security Hub Custom Framework',
                            controlSets=controlSets_List)
   
    #Write the framework id to the parameter
    frameworkid = response_framework['framework']['id']
    # write to ssm parameter store
    ssm.put_parameter(Name='CustomSecurityHubFrameworkID', Type='String', Value=frameworkid, Overwrite=True)
    print('frameworkId is ' + frameworkid)
    
    cfnsend(event, context, 'SUCCESS', responseData)
    return 'SUCCESS'
    
    
            
