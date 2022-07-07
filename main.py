# import required libraries
import os
import json
from datetime import datetime

# import google cloud library
from google.cloud import secretmanager
from google.cloud import storage

# read configuration file
f = open("config.json", "r")
data = json.load(f)
project_id = data.get("project_id")
secret_name = data.get("secret_name")

# generate new bucket name
year_date = datetime.now().strftime("%Y")
new_bucket_name = f"{project_id}" + "-data-injection-bucket-" + year_date
print(new_bucket_name)


secret_client = secretmanager.SecretManagerServiceClient()

request = {"name" : f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
response = secret_client.access_secret_version(request)
secret_value = response.payload.data.decode("UTF-8")

print(f"secret value : {secret_value}")

# bucket_name = "your-new-bucket-name"

def create_gcs_bucket(bucket_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="ASIA-SOUTH1")

    print("Created bucket {} in {} with storage class {}".format(new_bucket.name, new_bucket.location, new_bucket.storage_class))

    return new_bucket

# check wheather bucket has been created or not

def check_list_of_buckets(bucket_name):
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    if buckets.len() == 0:
        return create_gcs_bucket(bucket_name) 
    else:    
        for bucket in buckets:
            if bucket_name == bucket.name:
                return bucket
        else:
            return create_gcs_bucket(bucket_name) 

# hit url using api and get response

# store response into bucket

# entry-point function

def hello_pubsub(event, context):
    terget_bucket = check_list_of_buckets(bucket_name=new_bucket_name)