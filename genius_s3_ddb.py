import boto3

# DDB table
dynamodb = boto3.resource('dynamodb')
table_name = 'genius-table'

table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'user_id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print(f"DDB table '{table_name}' created!")

# S3 bucket
s3 = boto3.client('s3')
bucket_name = 'genius-bucket-654654514107'
s3.create_bucket(Bucket=bucket_name)

print(f"S3 bucket '{bucket_name}' created!")