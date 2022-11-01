# uber-movement-de

# 1. Architecture

![uber_architecture](https://user-images.githubusercontent.com/71977151/199323980-0722fc5e-5867-4198-b408-ff695d4cde03.png)

Pipeline consist of various phases
  1. Connection Phase - where data usually comes in. Push JSON into API.
  2. Streaming Phase - Using Amazon Kinesis to ingest real-time data.
  3. Raw Storage Phase - Store data as raw as possible in S3, because data is not ready for analytics.
  4. Processing Phase - When a new data file is uploaded in S3, AWS Lambda will trigger a glue crawler for populating the data table with new records and a glue job will be triggered for processing the data further. Since most of our reads are going to be analytical queries, it can be beneficial to transform the data into a columnar format i.e. parquet files. The parquet format reduces the amount of data scanned during query time. In this phase, Data Compaction is not included.
  5. Processed Data Storage Phase - Stores data that is cleaned and in parquet format because offers better compression of the data
  6. Golden Phase (NOT INCLUDED IN THE SOLUTION) - Next phase is to store data in the Golden layer which will be Amazon Redshift or data warehouse in order to write read-optimized analytical queries.
  
  
 # 2. Data Source
 
 Uber Movement Data
 Link: https://data.world/rmiller107/travel-time-uber-movement
 
 # 3. Setup
 
 1. Create AWS Account: https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fus-east-1.console.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26nc2%3Dh_ct%26region%3Dus-east-1%26skipRegion%3Dtrue%26src%3Dheader-signin%26state%3DhashArgsFromTB_us-east-1_40111e73ff4c98a0&client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&forceMobileApp=0&code_challenge=hNC1-nNstpJftOqnB-MOtclQOVEhIbI28fdqGooWVTU&code_challenge_method=SHA-256
 2. Download AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY. In Windows, Create .aws folder in C:\Users\.aws and create two files named config and credentials. config file contains the region_name and credentials file contains AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY.
 3. Create an Amazon Kinesis Data stream with the minimum setup and Kinesis Delivery Stream and select S3 as the destination.
 4. Attach the proper policies to Kinesis, in order to write data into S3.
 5. In AWS Glue, create a database and glue crawler.
 6. Create a Lambda function and copy the crawler_trigger.py into the newly created lambda function. Add trigger, when a file is uploaded into S3, the crawler_trigger lambda function will start executing the glue crawler and populating the already created database in the glue catalog.
 7. Create a CloudWatch Rule, when new data is added to the glue catalog, a lambda function named `trigger_gluejob` will start to trigger a glue job named `uber-gluejob`.
 8. All the necessary policies should be attached, most of them were: AmazonS3FullAccess, AWSGlueServiceRole and CloudWatchFullAccess.
 9. Run pip install -requirements.txt in order to install the python libraries. 
 
# 4. How to Run?
Once every AWS Service is setup, how to run the code?
1. The first script is initial_insert.py, we stimulate streaming by taking lines of CSV, turning them to JSON, and pushing them to Kinesis Data Stream. Once this script is started, the other scripts such as crawler_trigger.py, trigger_gluejob.py, and uber_gluejob.py will be run in consecutive order.
2. The second script is stream.py, with this script we post data to API, and the data that is coming from the API is going to be written into the Kinesis data stream.


