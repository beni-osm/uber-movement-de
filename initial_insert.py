# AWS Libraries
import boto3

# Data Processing Libraries
import json
import numpy as np
import pandas as pd

# AWS Config
kinesis = boto3.client('kinesis')
stream_name = 'uber-movement-stream'

# Data Config
PARTITION_KEY = 'Origin Movement ID'
COLUMNS_CHECK = ['Origin Geometry', 'Destination Geometry']
COLUMN_ORDER = ['Origin Movement ID', 'Origin Display Name', 'Origin Geometry',
                'Destination Movement ID', 'Destination Display Name',
                'Destination Geometry', 'Date Range', 'Mean Travel Time (Seconds)',
                'Range - Lower Bound Travel Time (Seconds)',
                'Range - Upper Bound Travel Time (Seconds)']


def column_check(data_table: pd.DataFrame, columns: list):
    """
    Check if particular columns are part of the data table.

    :parameters
        data_table: dataframe that needs to check its columns.
        columns: list of columns

    :returns data_table: dataframe to be returned.
    """
    for column in columns:
        if column not in data_table.columns:
            data_table[column] = np.nan
    return data_table[COLUMN_ORDER]


def concatenate_datatables(data_tables: list):
    """
    Concatenating multiple table into one result table because they have the same columns.

    :params data_tables: List of dataframe.
    :returns result: Result dataframe created by concatenating multiple dataframes.
    """
    return pd.concat(data_tables)


def put_records_to_kinesis(result_json: list):
    """
    Put Record to data stream

    :params result_json: list of dictionaries
    :return:
    """
    for record in result_json:
        response = kinesis.put_record(StreamName=stream_name, Data=json.dumps(record),
                                      PartitionKey=PARTITION_KEY)
        print(response)


if __name__ == "__main__":
    bogota = pd.read_csv("./data/Travel_Times - Bogota.csv")
    boston = pd.read_csv("./data/Travel_Times - Boston.csv")
    johburg_pretoria = pd.read_csv("./data/Travel_Times - Johannesburg and Pretoria.csv")
    manila = pd.read_csv("./data/Travel_Times - Manila.csv")
    paris = pd.read_csv("./data/Travel_Times - Paris.csv")
    sydney = pd.read_csv("./data/Travel_Times - Sydney.csv")
    washington_dc = pd.read_csv("./data/Travel_Times - Washington DC.csv")

    # Column check
    bogota = column_check(bogota, COLUMNS_CHECK)
    boston = column_check(boston, COLUMNS_CHECK)
    johburg_pretoria = column_check(johburg_pretoria, COLUMNS_CHECK)
    manila = column_check(manila, COLUMNS_CHECK)
    paris = column_check(paris, COLUMNS_CHECK)
    sydney = column_check(sydney, COLUMNS_CHECK)
    washington_dc = column_check(washington_dc, COLUMNS_CHECK)

    # Concatenate dataframes
    result_table = concatenate_datatables(
        [bogota, boston, johburg_pretoria, manila, paris, sydney, washington_dc])

    result_table = result_table[:1000]
    # Convert dataframe to json
    result_json = json.loads(result_table.to_json(orient='records'))

    # Put record to kinesis data stream
    put_records_to_kinesis(result_json)
