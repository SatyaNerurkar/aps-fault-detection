import json
import pymongo
import pandas as pd

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

# Database Name
DATABASE_NAME = "aps_data"

# Collection  Name
COLLECTION_NAME = "Sensor"

# CSV file path
DATA_FILE_PATH = "/config/workspace/aps_failure_training_set1.csv"

if __name__ == "__main__":
    # creating dataframe
    df = pd.read_csv(DATA_FILE_PATH)

    #Display 1st record from csv file
    print(f"Rows and columns: {df.shape}")

    # convert dataframe to json format
    df.reset_index(drop=True, inplace=True)

    # Transforming dataset
    json_record = list(json.loads(df.T.to_json()).values())

    # Display 1st record from json file
    print(json_record[0])

    # insert data to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)