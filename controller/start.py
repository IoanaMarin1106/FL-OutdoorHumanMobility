import requests
import time
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# get AWS credentials
bucket_name = os.environ.get("BUCKET_NAME")
aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

endpoint = "http://localhost:5000"

s3_client = boto3.client(
    's3',
    region_name='eu-north-1',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url='https://s3.eu-north-1.amazonaws.com'
)


if __name__ == '__main__':
    while True:
        response = requests.get(f'{endpoint}/start_train')
        subfolder = response.content.decode("utf-8")
        # subfolder looks like '15-01-2024-140507493138'
        train_session_id = subfolder.split('/')[-1]

        print(f'Started training session with id={train_session_id}, waiting 2min for checkpoints.')

        time.sleep(20)

        objects = s3_client.list_objects(Bucket=bucket_name)
        checkpoints = list(filter(lambda obj: obj['Key'].startswith(f'clients_checkpoints/{subfolder}') and obj['Key'].endswith('.ckpt'), objects['Contents']))
        checkpoint_names = list(map(lambda c: c['Key'], checkpoints))

        print(f'Found {len(checkpoint_names)} checkpoints in this training session. Starting FedAvg process.')

        # Perform FedAvg...

        print(f'Finished FedAvg process. Uploading agg_checkpoint.ckpt to S3 bucket.')

        s3_client.upload_file(Filename="/Users/eciurezu/work/school/fl-outdoor-human-mobility/controller/checkpoint.ckpt", Bucket=bucket_name, Key=f'server_checkpoints/{train_session_id}/agg_checkpoint.ckpt')

        print('Sending download notification to clients.')
        requests.get(f'{endpoint}/send_checkpoint/{train_session_id}')

        print(f'Finished training session with id={train_session_id}.')
        print('Waiting 2h until next training session...')

        time.sleep(2 * 60 * 60)
