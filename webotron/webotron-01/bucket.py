import mimetypes
from pathlib import Path
from botocore.exceptions import ClientError
import util
'''classes for s3 buckets'''
class BucketManager:
    '''Manage an S3 bucket'''
    def __init__(self,session):
        #self.name=name
        self.session=session
        self.s3=self.session.resource('s3')

    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        client = self.s3.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host)    










    def all_buckets(self):
        '''Get an iterator of all buckets'''
        return self.s3.buckets.all()


    def all_objects(self,bucket):
        '''Get an iterator for all objects in bucket'''
        return self.s3.Bucket(bucket).objects.all()

    def init_bucket(self,bucket):
        "Set up and configure S3 bucket"
        s3_bucket=None
        try:
             s3_bucket=self.s3.create_bucket(Bucket=bucket,CreateBucketConfiguration=
         {'LocationConstraint':'us-east-2'})

        except ClientError as e:
            if e.response['Error']['Code']== 'BucketAlreadyOwnedByYou':
                    s3_bucket=self.s3.Bucket(bucket)
            else :
                    raise e
        return s3_bucket

    def set_policy(self,bucket):
        policy='''{
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
            "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
          ]
        }
        ]
        }'''%bucket.name					#policy for website
        pol=bucket.Policy()
        pol.put(Policy=policy)


    def configure_website(self,bucket):
        ws=bucket.Website()
        ws.put(WebsiteConfiguration={'ErrorDocument':{'Key':'error.html'},'IndexDocument':{'Suffix':'index.html'}})
    def upload_file(self,bucket,path,key):
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(path,key,ExtraArgs={'ContentType':'text/html'})

    def sync(self,pathname,bucket):
        bucket=self.s3.Bucket(bucket)
        root=Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket,str(p),str(p.relative_to(root)))
                    #print("Path:{}\n Key:{}".format(p,p.relative_to(root)))
        handle_directory(root)
