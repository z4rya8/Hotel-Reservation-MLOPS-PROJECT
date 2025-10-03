from google.cloud import storage

client = storage.Client()
bucket = client.bucket("my_bucket1776")
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.name)

