import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from datetime import datetime

import boto3

client = boto3.client('s3')

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def create_folder():
    response = client.put_object(
        Bucket='uber-movement-processed-data',
        Body='',
        Key=f'{processed_folder}/'
    )
date_time = datetime.now()
processed_folder = str(date_time.year) + '_' + str(date_time.month) + '_' + str(date_time.day) + '_' + str(
    date_time.hour)

# Check if the folder exists
result = client.list_objects_v2(Bucket='uber-movement-processed-data', Prefix=processed_folder)

if 'Contents' in result:
    print("Key exists in the bucket.")
else:
    print("Key doesn't exist in the bucket.")
    create_folder()

# Reading data from glue catalog
uber_data = glueContext.create_dynamic_frame.from_catalog(database = "uber-movement-data", table_name = "uber_movement_raw_data", transformation_ctx = "datasource0").toDF()

# Using relevant columns
uber_data = uber_data.select('Origin Movement ID', 'Origin Display Name', 'Origin Geometry',
                             'Destination Movement ID', 'Destination Display Name',
                             'Destination Geometry', 'Date Range', 'Mean Travel Time (Seconds)',
                             'Range - Lower Bound Travel Time (Seconds)',
                             'Range - Upper Bound Travel Time (Seconds)')

# Converting dataframe to DynamicFrame
uber_movement_frame = DynamicFrame.fromDF(uber_data, glueContext, "uber_movement_data")

# Write the new version of the data in processed zone.
uber_data_sink = glueContext.write_dynamic_frame.from_options(frame = uber_movement_frame, connection_type = "s3", 
                                                        connection_options = {"path": f"s3://uber-movement-processed-data/{processed_folder}/"}, format = "parquet", transformation_ctx = "uber_data_sink")
job.commit()
