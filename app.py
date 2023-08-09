import boto3
import requests

url = 'http://127.0.0.1:5000/getNoOfRecs'

num_of_rows = requests.get(url).text

print(num_of_rows)

text_file = open("file_to_upload.txt", "w")
n = text_file.write(num_of_rows)
text_file.close()

OBJECT_NAME_TO_UPLOAD = 'file_to_upload.txt'

s3_client = boto3.client('s3')

# Generate the presigned URL
response = s3_client.generate_presigned_post(
    Bucket='ttomczyk-bucket-ups006',
    Key=OBJECT_NAME_TO_UPLOAD,
    ExpiresIn=10
)

print(response)

# Upload file to S3 using presigned URL
files = {'file': open(OBJECT_NAME_TO_UPLOAD, 'rb')}
r = requests.post(response['url'], data=response['fields'], files=files)
print(r.status_code)
