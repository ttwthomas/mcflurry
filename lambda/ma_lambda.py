import lol as resto
from os import getenv
import time, json
import boto3
import botocore

def upload_file_to_s3(file_name,bucket):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, "missingflurry.js", ExtraArgs={'ACL':'public-read','ContentType': "application/javascript"})
    except botocore.exceptions.ClientError as error:
        print(error)
        return False
    return True

def create_invalidation():
    cf = boto3.client('cloudfront')
    res = cf.create_invalidation(
        DistributionId = getenv("DISTRIBUTIONID"),
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/missingflurry.js']
            },
            "CallerReference": str(time.time()).replace(".", "")
        }
    )
      
    return True


def lambda_handler(event, context=None):
    print(event)
    restaurants = resto.load_restaurants()
    limit = int(getenv("LIMIT") ) if getenv("LIMIT") else None
    restaurants_menu = resto.get_unavailable_menu(restaurants[:limit])
    resto.save_restaurants_menu_json(restaurants_menu,"/tmp/missingflurry.js") # create missingflurry.json
    result = upload_file_to_s3("/tmp/missingflurry.js", "mcflurry.cocadmin.com")
    create_invalidation()
    response = {
        "statusCode": 200,
        "body": json.dumps(str(result))
    }
    return response
    
if __name__ == "__main__":
    test_event = {
        "body": "eyJ0ZXN0IjoiYm9keSJ9",
        "resource": "/{proxy+}",
        "path": "/path/to/resource",
        "httpMethod": "POST",
        "isBase64Encoded": True,
        "queryStringParameters": {
            "username": "basdasdaar"
        },
        "multiValueQueryStringParameters": {
            "username": [
            "basdasdaar"
            ]
        },
        "pathParameters": {
            "proxy": "/path/to/resource"
        },
        "stageVariables": {
            "baz": "qux"
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ],
            "Accept-Encoding": [
            "gzip, deflate, sdch"
            ],
            "Accept-Language": [
            "en-US,en;q=0.8"
            ],
            "Cache-Control": [
            "max-age=0"
            ],
            "CloudFront-Forwarded-Proto": [
            "https"
            ],
            "CloudFront-Is-Desktop-Viewer": [
            "true"
            ],
            "CloudFront-Is-Mobile-Viewer": [
            "false"
            ],
            "CloudFront-Is-SmartTV-Viewer": [
            "false"
            ],
            "CloudFront-Is-Tablet-Viewer": [
            "false"
            ],
            "CloudFront-Viewer-Country": [
            "US"
            ],
            "Host": [
            "0123456789.execute-api.us-east-1.amazonaws.com"
            ],
            "Upgrade-Insecure-Requests": [
            "1"
            ],
            "User-Agent": [
            "Custom User Agent String"
            ],
            "Via": [
            "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
            ],
            "X-Amz-Cf-Id": [
            "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
            ],
            "X-Forwarded-For": [
            "127.0.0.1, 127.0.0.2"
            ],
            "X-Forwarded-Port": [
            "443"
            ],
            "X-Forwarded-Proto": [
            "https"
            ]
        },
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "requestTime": "09/Apr/2015:12:34:56 +0000",
            "requestTimeEpoch": 1428582896000,
            "path": "/prod/path/to/resource",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "apiId": "1234567890",
            "protocol": "HTTP/1.1"
        }
        }
    lambda_handler(test_event)
