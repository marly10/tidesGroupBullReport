#!/usr/bin/env python3

import boto3
from datetime import *

AWS_REGION = "us-east-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
instances = EC2_RESOURCE.instances.all()

launch_time_list = []

for instance in instances:
#  print(f'EC2 instance {instance.id}” information:')
#  print(f'Instance Name: {instance.state["Name"]}')
#  print(f'Instance AMI: {instance.image.id}')
#  print(f'Instance platform: {instance.platform}')
#  print(f'Instance type: “{instance.instance_type}')
 #print(f'EC2 Launch Time: {instance.launch_time}')
 launch_time_list.append(instance.launch_time)
 #print('-'*60)
string = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\s+[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\+[0-9][0-9]:[0-9][0-9]'
for i in launch_time_list:
    print(f'EC2 Launch Time - ARRAY1: {i}')
    print('-'*40)
    
    # dt = datetime(i)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    # print(f'EC2 Launch Time - ARRAY2: {i}')
    # print('-'*60)
    lt_datetime = datetime.strptime(str(i), string)
    lt_delta = datetime.utcnow() - str(lt_datetime)
    uptime = str(lt_delta)
    print(uptime)
    
# 2019-08-23T17:19:01.89	