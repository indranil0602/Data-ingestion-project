# import required libraries
import os
from datetime import datetime

# import google cloud library
from google.cloud import secretmanager
from google.cloud import storage

today_date = datetime.now().strftime("%Y-%m-%d")
bucket_name = "data-injection-bucket-gcs-ip"
print(bucket_name)


client = secretmanager.SecretManagerServiceClient()

f = open("config.json", "r")
data = json.load(f)
project_id = data.get("project_id")
secret_name = data.get("secret_name")

request = {"name" : f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
response = client.access_secret_version(request)
secret_value = response.payload.data.decode("UTF-8")

print(f"secret value : {secret_value}")

# bucket_name = "your-new-bucket-name"

def create_gcs_bucket(bucket_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )

# check wheather bucket has been created or not

def check_list_of_buckets(bucket_name):
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    if buckets.len() == 0:
        create_gcs_bucket(bucket_name) 
    else:    
        for bucket in buckets:
            if bucket_name == bucket.name:
                return
        else:
            create_gcs_bucket(bucket_name) 

# hit url using api and get response

# store response into bucket

# entry-point function

check_list_of_buckets(bucket_name=bucket_name)