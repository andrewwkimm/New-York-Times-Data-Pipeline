import os
import pandas as pd
from google.cloud import storage
import config

# Connect to the client and set the bucket name
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_cloud_key.json'
storage_client = storage.Client()
bucket_name = 'new-york-times-bucket'
bucket = storage_client.bucket(bucket_name)

def download_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception:
        return False

def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception:
        return False

def update_upload_file():
    # Set both the current data in the bucket and the data pulled through DAG
    df_today = pd.read_csv(config.file_path_today)
    df_yesterday = pd.read_csv(config.file_path_yesterday)

    # Set in the records from today's data to yesterday's
    df_final = pd.concat([df_yesterday, df_today])
    # Remove duplicate rows
    df_final.drop_duplicates()
    # Output the final file to be uploaded
    df_final.to_csv(config.file_path, index = False)
    return 0

def main():
    download_from_bucket('nyt_data', config.file_path_yesterday, 'new-york-times-bucket')
    update_upload_file()
    upload_to_bucket('nyt_data', config.file_path, 'new-york-times-bucket')

if __name__ == "__main__":
    main()

