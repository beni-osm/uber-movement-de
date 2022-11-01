# AWS Libraries
import boto3

# AWS Config
glue = boto3.client('glue')
CRAWLER_NAME = 'uber-movement-crawler-raw'


def lambda_handler(event, context):
    response = glue.start_crawler(
        Name=CRAWLER_NAME
    )
    return {
        'statusCode': 200,
    }
