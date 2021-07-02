#  CustomAuditManagerFramework Lambda 
#  - Creates Custom Audit Manager Control Sets and Custom Audit Manager Framework based on AWS Config Conformance Pack
#  ---Takes a csv input that lists all Config rules in a Conformance Pack. For e.g. NIST-CSF as an example input here
#  
#
# @kmmahaj
#
## License:
## This code is made available under the MIT-0 license. See the LICENSE file.


import json
import codecs
import copy
import sys
import datetime
import boto3
import botocore
import time
import logging
import random
import urllib3
import csv
import os
from csv import reader
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


def create_custom_auditmanager_control(controls):
    
    auditmanager = boto3.client('auditmanager')
    configconfpackcontrol_List= []
    control_id =""
    controltype = controls[0]
    controllist = controls[1:]
    
    #Create a Custom Config Conformance Pack Control Source - Config Conf Pack Control Source
    configconfpack_controlmappingsource_template = {}
    configconfpack_controlmappingsource_template['sourceName'] = 'Custom Config Conformance Pack Control Source'
    configconfpack_controlmappingsource_template['sourceDescription'] = 'Conformance Pack checks'
    configconfpack_controlmappingsource_template['sourceSetUpOption'] = 'System_Controls_Mapping'
    configconfpack_controlmappingsource_template['sourceType'] = 'AWS_Config'
    sourceKeyword = {
                'keywordInputType': 'SELECT_FROM_LIST',
                'keywordValue': 'Conformance Pack checks'
            }
    configconfpack_controlmappingsource_template['sourceKeyword'] = sourceKeyword
    
    for controlname in controllist:
        configconfpack_controlmappingsource = copy.deepcopy(configconfpack_controlmappingsource_template)
        configconfpack_controlmappingsource['sourceKeyword']['keywordValue'] = controlname
        configconfpackcontrol_List.append(configconfpack_controlmappingsource)
        
        
    #Create a Custom Config Conformance Pack Control
    name = controltype + '-CustomConfigConfpackControl'
    response_control = auditmanager.create_control(name=name, controlMappingSources=configconfpackcontrol_List)
    control_id = response_control['control']['id']
    
    return control_id

def create_custom_auditmanager_controlset(controlslist):
    

    complianceframework_controls_controlid = create_custom_auditmanager_control(controlslist)
    
    #Add to a Custom NIST Config Conformance Pack Control Set   
    configconfpack_complianceframework_controlset = {}
    configconfpack_complianceframework_controlset['name'] = 'ControlSet- ' + controlslist[0]
    configconfpack_complianceframework_controlset['controls'] = []
    configconfpack_controldict ={}
    configconfpack_controldict['id'] = complianceframework_controls_controlid
    configconfpack_complianceframework_controlset['controls'].append(configconfpack_controldict)
    
    return configconfpack_complianceframework_controlset
    

def lambda_handler(event, context):
   
    print ("boto3 version: " +  boto3.__version__)
    auditmanager = boto3.client('auditmanager')
    ssm = boto3.client('ssm')
    s3 = boto3.client('s3')
    

    logger.info('EVENT Received: {}'.format(event))
    responseData = {}
    controlSets_List =[]
      
    S3Bucket = os.environ['S3Bucket']
    MappingFile = os.environ['MappingFile']

    #Handle cfnsend delete event
    eventType = event['RequestType']
    if eventType == 'Delete':
        logger.info(f'Request Type is Delete; unsupported')
        cfnsend(event, context, 'SUCCESS', responseData)
        return 'SUCCESS'
    
  
    #Create a NIST Control Set
    data = s3.get_object(Bucket=S3Bucket, Key=MappingFile)
    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        controlslist =[]
        for value in row.values():
            if value != 'none':
                controlslist.append(value)
        controlSets_List.append(create_custom_auditmanager_controlset(controlslist))


    #Create a NIST Control Set
    #with open('nistmapping.csv', 'r') as read_obj:
    #    csv_reader = reader(read_obj)
    #    for row in csv_reader:
    #        controlSets_List.append(create_custom_auditmanager_controlset(row))

    #Create a Custom Config Conformance Pack Framework for NIST controls
    
    response_framework = auditmanager.create_assessment_framework(name='Config Conformance Pack Custom Framework',
                            controlSets=controlSets_List)
   
    #Write the framework id to the parameter
    frameworkid = response_framework['framework']['id']
    # write to ssm parameter store
    ssm.put_parameter(Name='CustomConfigConformancePackFrameworkID', Type='String', Value=frameworkid, Overwrite=True)
    print('frameworkId is ' + frameworkid)
    
    cfnsend(event, context, 'SUCCESS', responseData)
    return 'SUCCESS'
    