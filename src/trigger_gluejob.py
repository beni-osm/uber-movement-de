# AWS Libraries
import boto3

# AWS Congi
glue = boto3.client('glue')
GLUE_JOB = 'uber-gluejob'

def lambda_handler(event, context):
    response = glue.start_job_run(JobName=GLUE_JOB)
    return {
        'statusCode': 200,
    }