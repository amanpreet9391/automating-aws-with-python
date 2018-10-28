# coding: utf-8
import boto3
session=boto3.Session(profile_name='python_automation')
as_client=session.client('autoscaling')
as_client.execute_policy(AutoScalingGroupName='Notifon example group',PolicyName='Scale Up')
