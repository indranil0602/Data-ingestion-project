# import required libraries
import os
import json
import base64
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

# getting secrets from secret-manager
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
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
  
    for bucket in buckets:
        if bucket_name == bucket.name:
            return True
    return False

# hit url using api and get response

# store response into bucket
def upload_file_to_gcs(bucket_name, source_file_name, destination_file_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    print("File {source_file_name} uploaded to {destination_file_name}")

# entry-point function

def hello_pubsub(event, context):
    #check bucket and get terget bucket
    target_bucket_name = ""
    
    if check_list_of_buckets(bucket_name=new_bucket_name) != True:
        target_bucket_name = create_gcs_bucket(new_bucket_name).name

    #call api and get the response

    #upload responses into terget bucket
    upload_file_to_gcs(bucket_name=terget_bucket_name, source_file_name, destination_file_name)

    print("Done")