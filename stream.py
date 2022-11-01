# AWS Libraries
import boto3

# Flask
from flask import Flask, jsonify, request

# Data Processing Libraries
import json

app = Flask(__name__)

# AWS Config
kinesis = boto3.client('kinesis')
stream_name = 'uber-movement-stream'

# Data Config
PARTITION_KEY = 'Origin Movement ID'

def put_records_to_kinesis(record_json: dict):
    """
    Put Record to data stream

    :params result_json: list of dictionaries
    :return:
    """

    response = kinesis.put_record(StreamName=stream_name, Data=json.dumps(record_json),
                                      PartitionKey=PARTITION_KEY)
    print(response)

@app.route("/uber_movement", methods=['POST'])
def uber_movement():
    # Get data
    record_json = request.get_json()
    #Put data into kinesis stream
    put_records_to_kinesis(record_json)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
