import pytest
import botocore
from botocore.stub import Stubber
import boto3
from datetime import datetime
from ecshelpers.boto_session_creator import botoSessionCreator as bsc


@pytest.mark.aws_integration
def test_fetch_sessions_from_s3(assertions):
    session_creator = bsc(False)
    s3_bucket_name = "tjanusz-personal-demo-stuff"
    s3_object_key = "dockerImagesSecInfo/accountsToProcess.csv"
    base_infos = session_creator.fetch_sessions_from_s3(s3_bucket_name, s3_object_key)
    assertions.assertEqual(3, len(base_infos))

@pytest.mark.aws_integration
def test_fetch_sessions_from_s3_throws_error_with_bad_key(assertions):
    session_creator = bsc(False)
    s3_bucket_name = "tjanusz-personal-demo-stuff"
    s3_object_key = "dockerImagesSecInfo/bad_key_name"
    with pytest.raises(botocore.exceptions.ClientError) as exec_info:
        session_creator.fetch_sessions_from_s3(s3_bucket_name, s3_object_key)

    assertions.assertEqual(exec_info.typename, "NoSuchKey")

@pytest.mark.aws_integration
def test_fetch_sessions_from_s3_throws_error_with_bad_bucket_name(assertions):
    session_creator = bsc(False)
    s3_bucket_name = "tjanusz-personal-demo-stuff2"
    s3_object_key = "dockerImagesSecInfo/bad_key_name"
    with pytest.raises(botocore.exceptions.ClientError) as exec_info:
        session_creator.fetch_sessions_from_s3(s3_bucket_name, s3_object_key)
    assertions.assertEqual(exec_info.typename, "NoSuchBucket")

def test_create_session_from_info_returns_boto_session_with_assumed_role_from_sts(assertions):
    session_creator = bsc(False)
    boto_sts=boto3.client('sts')
    stubber = Stubber(boto_sts)
    stubbed_info = {
        'role_arn': 'arn:aws:sts::123456789012:assumed-role/Infosec-Role/ImageScanner',
        'account_id': '111111111',
        'region_name': 'us-east-1'
    }
    stub_response = {
        'Credentials':
            {
                'AccessKeyId': '1x1x1x1x1x1x1x1x1x1x',
                'SessionToken' : '2x2x2x2x2x2x2x2x',
                'SecretAccessKey' : '3x3x3x3x3x3x3x3x',
                'Expiration': datetime(2015, 1, 1)
            }
    }
    expected_params = {
        'RoleArn': stubbed_info['role_arn'],
        'RoleSessionName': 'newsession'
    }

    stubber.add_response('assume_role', stub_response, expected_params)
    stubber.activate()
    results = session_creator.create_session_from_info(stubbed_info, boto_sts)
    stubber.deactivate()
    # assert our creds were created inside the session and credentials objects
    assertions.assertEqual(pull_out_creds(results, 'access_key'), "1x1x1x1x1x1x1x1x1x1x")
    assertions.assertEqual(pull_out_creds(results, 'secret_key'), "3x3x3x3x3x3x3x3x")
    assertions.assertEqual(pull_out_creds(results, 'token'), "2x2x2x2x2x2x2x2x")

def pull_out_creds(results, cred_attr): 
    return results.__getattribute__('_session').__getattribute__('_credentials').__getattribute__(cred_attr)