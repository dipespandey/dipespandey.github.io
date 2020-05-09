---
layout: post
title: "Designing a serverless data management platform"
author: "Dipesh"
---

In recent times, I am working with an early-stage startup that specializes in Ads data aggregation and analysis
to help the companies optimize their budgets through targeted insights. As a starting member of the development team,
I took the responsibility to design the serverless architecture in AWS. After trying a few things here and there, we have
come to use these awesome tools in AWS for the product:  

1. API Gateway

2. Lambda Functions

3. DynamoDb

4. S3

I will explain each of them briefly below and try to show the complete picture of how these components interact with each other.

Because this is going to be a SaaS, we are going to expose API endpoints to our clients where they can connect their Ad accounts and allow us to collect their data. We, in turn, will produce insights from the data and help them make better use of their budget
through Targeted Ads Placement.

To ensure we have a stable system, we need streaming and scheduling abilities in the product. I have approached these in the following ways.

1. Streaming
We need the capability to stream data from the Ad accounts (eg. Google, Facebook, Youtube, et. al.) up to the S3 buckets so that this data can be used for analysis in the later stage. The obvious choice was Kinesis as it has in-built configuration options for source and sinks. But we chose the lighter and more configurable tool in DynamoDb which has got it's own streaming triggers using Lambda. Also, the cost analysis helped us favor DynamoDb upfront.

2. Scheduling
Apart from streaming, we also need the capability to schedule the stream. For this, there are a lot of great options available including the likes of AirFlow, Celery, et. al. We have, however, chosen Cloudwatch Events (I think they now call it EventBridge) triggering a lambda function, this being called by an API endpoint. This would mean we could create custom schedules from the API. 

```python

import json
import boto3

cloudwatch_events = boto3.client('events')
lambda_client = boto3.client('lambda')


def schedule_event(schedule_object):
    # Create a scheduled rule
    lambda_name = 'markaiter-api-to-dyn'
    rule_response = cloudwatch_events.put_rule(Name='DATA_EXTRACTION_EVENT',  
                                               RoleArn='',  
                                               ScheduleExpression='custom_schedule_expression',  
                                               State='ENABLED')  
    rule_name = "DATA_EXTRACTION_EVENT"  

    # Add permission to lambda
    lambda_client.add_permission(FunctionName='api-to-dynamodb',  
                                    StatementId="{0}-Event".format(rule_name),  
                                    Action='lambda:InvokeFunction',  
                                    Principal='events.amazonaws.com',  
                                    SourceArn=rule_response['RuleArn'])  

    # Add a lambda function target
    # Put target for rule
    schedule_response = cloudwatch_events.put_targets(Rule=rule_name,  
                                                    Targets=[  
                                                        {  
                                                            'Arn': f'function_arn',  
                                                            'Id': 'EventsTargetID',  
                                                            'Input': json.dumps(schedule_object)  
                                                        }])  
    return schedule_response  

```

The code is pretty much self-explanatory. What we do is we pass the schedule_object through the API. This triggers a cloudwatch event which in turn triggers a lambda function according to the schedule passed in. The lambda function does the intended task to collect data and send it to DynamoDb.

DynamoDb is configured in such a way that any incoming data would trigger another lambda function which would send it to S3. S3, here, is our final sink. We can now use to query data from S3 and apply the necessary machine learning models to generate insights for the clients.  

This is what we have already done to some extent. We still have been facing the Google and Facebook API Authorization Access issue having applied for the access for about a month now. If you have any tips regarding the API access, please let me know. Also, if you think there are any red flags in this approach or if there's something you would want to suggest, I would be happy to incorporate them.