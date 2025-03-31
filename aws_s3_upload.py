import boto3

# Initialize a session using AWS credentials (make sure your AWS CLI is configured)
s3_client = boto3.client('s3')

# Upload the JSON file to the S3 bucket
s3_client.upload_file('card_details.json', 'your-bucket-name', 'card_details.json')

print("JSON file uploaded to S3 successfully!")
