import boto3
import botocore
from logger import Logger


class AWSResponse:
    def __init__(self, success=False, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

    
def operation_handler(operation):
    try:
        result = operation()
        return AWSResponse(data=result, success=True)
    except botocore.exceptions.ClientError as error:
        return AWSResponse(error=error, success=False)


class AWSS3:
    def __init__(self, access_key_id, secret_access_key):
        self.s3_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)
        self.resource = self.s3_session.resource('s3')
    
    
    def upload_file(self, destination, bucket_name, prefix):
        """
        prefix: is the name of the file.
        destination: is the complete path.
        """
        def operation():
            my_bucket = self.resource.Bucket(bucket_name)
            my_bucket.upload_file(destination, prefix)
            return True
        return operation_handler(operation)


    def download_file(self, bucket_name, prefix, destination):
        """
        prefix: is the name of the file.
        destination: is the complete path.
        """
        def operation():
            my_bucket = self.resource.Bucket(bucket_name)
            my_bucket.download_file(prefix, destination)
            return True
        return operation_handler(operation)


    def list_files(self, bucket_name, prefix):
        def operation():
            my_bucket = self.resource.Bucket(bucket_name)
            files = my_bucket.objects.filter(Prefix=prefix)
            files = list(map(lambda f: f.key, files))
            return files
        return operation_handler(operation)

    
    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name


    def set_session(self, access_key_id, secret_access_key):
        self.s3_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        self.resource = self.s3_session.resource('s3')
