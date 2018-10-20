#!/usr/bin/python
#-*- coding: utf-8 -*-
'''Webotron:deploy website with aws.'''
#pipenv install boto3
import boto3

import click


import mimetypes
from bucket import BucketManager

#s3=session.resource('s3')
##bucket_manager=None
#@click.group()
#@click.option('--profile',default=None,help="use a given aws profile")
#def cli(profile):
    #"Webotron deploys website to AWS"
    #global session,bucket_manager
    #session_cfg={}
    #if profile:
        #session.cfg['profile_name']=profile
    #session=boto3.Session(**session_cfg)
@click.group()
@click.option('--profile', default=None,
              help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager 

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    #domain_manager = DomainManager(session)
    #cert_manager = CertificateManager(session)
    #dist_manager = DistributionManager(session)
    #bucket_manager=BucketManager(session)








@cli.command("list-buckets")
def list_buckets():
    "List all S3 buckets"
    for bucket in bucket_manager.all_buckets():
        print(bucket)
@cli.command("list-bucket-objects")
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List objects in S3 buckets"
    for obj in bucket_manager.all_objects(bucket):
        print(obj)
@cli.command("setup-bucket")
@click.argument('bucket')

def setup_bucket(bucket):
    s3_bucket=bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return

@cli.command('sync')
@click.argument('pathname',type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
    "Sync content of pathname to buckets"
    s3_bucket=s3.Bucket(bucket)
    bucket_manager.sync(pathname,bucket)


if __name__ == '__main__':
    cli()
