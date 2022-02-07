import boto3
import csv

class botoSessionCreator:
    ''' Simple methods for doing cross account type session creating.'''

    def __init__(self, verbose_mode = False) -> None:
        self.verbose_mode = verbose_mode


    def fetch_sessions_from_s3(self, bucket_name, s3Key, s3_client = None) -> list[dict]:
        """
            retrieve the .csv file of our current valid AWS account info to pull from and return as an array of session info
        """

        # pull a csv file from s3 and open and return list
        if not s3_client:
            s3_client = boto3.client('s3')

        data = s3_client.get_object(Bucket=bucket_name, Key=s3Key)
        
        # read the contents of the file and split it into a list of lines
        lines = data['Body'].read().decode('utf-8').split()      
        
        session_infos = []
        for row in csv.DictReader(lines):
            session_info = { 
                'role_arn': row['role_arn'],
                'account_id': row['account_id'],
                'region_name': row['region_name']
            }
            session_infos.append(session_info)

        return session_infos

    def create_session_from_info(self, session_info: dict, boto_sts: boto3.client = None) -> boto3.Session:
        # pull out role and invoke STS assume role
        # https://www.slsmk.com/use-boto3-to-assume-a-role-in-another-aws-account/
        
        if not boto_sts:
            boto_sts=boto3.client('sts')

        sts_response = boto_sts.assume_role(
            RoleArn=session_info['role_arn'],
            RoleSessionName='newsession'
        )

        # Save the details from assumed role into vars
        new_session_id = sts_response["Credentials"]["AccessKeyId"]
        new_session_key = sts_response["Credentials"]["SecretAccessKey"]
        new_session_token = sts_response["Credentials"]["SessionToken"]

        boto_session = boto3.Session(aws_access_key_id=new_session_id, aws_secret_access_key=new_session_key, 
                aws_session_token=new_session_token, region_name=session_info['region_name'])
        return boto_session