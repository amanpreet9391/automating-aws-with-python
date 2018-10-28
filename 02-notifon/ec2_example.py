# coding: utf-8
import boto3
session=boto3.Session(profile_name='python_automation')
ec2=session.resource('ec2')
key_name='python_automation_key'
key_path=key_name +'.pem'
key=ec2.create_key_pair(KeyName=key_name)
key.key_material
key
python_automation_key
python_automation_key.key_material
key_name='aws_key'
key_path=key_name +'.pem'
key=ec2.create_key_pair(KeyName=key_name)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
get_ipython().run_line_magic('ls', '-l aws_key.pem')
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
import os,stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l aws_key.pem')
ec2.images.filter(Owners=['amazon'])
img=ec2.Image('ami-0ff8a91507f77f867')
img.name
ami_name='amzn-ami-hvm-2018.03.0.20180811-x86_64-gp2'
filters = [{'Name':'name','Values':[ami_name]}]
list(ec2.images.filter(Owners=['amazon'],Filters=filters))
img
key
instances=ec2.create_instances(ImageId=img.id,MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
instances
inst=instances[0]
inst.public_dns_name
inst.wait_until_running()
inst.reload()
inst.public_dns_name
inst.security_groups
sg=ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort':22,'ToPort':22,'IpProtocol':'TCP','IpRanges':[{'CidrIp':'220.227.229.77/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort':80,'ToPort':80,'IpProtocol':'TCP','IpRanges':[{'CidrIp':'0.0.0.0/0'}]}])
inst.public_dns_name
get_ipython().run_line_magic('history', '')
