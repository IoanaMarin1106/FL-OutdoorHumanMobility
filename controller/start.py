import requests
import time
import boto3
import os
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

# get AWS credentials
bucket_name = os.environ.get("BUCKET_NAME")
aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

endpoint = f'http://{os.environ.get("FL_SERVER_ENDPOINT")}:{os.environ.get("FL_SERVER_PORT")}'
frequency_hours = int(os.getenv("FREQUENCY_HOURS", '24'))
frequency_seconds = frequency_hours * 3600

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

        time.sleep(10)

        objects = s3_client.list_objects(Bucket=bucket_name)
        checkpoints = list(filter(lambda obj: obj['Key'].startswith(f'clients_checkpoints/{subfolder}') and obj['Key'].endswith('.ckpt'), objects['Contents']))
        checkpoint_names = list(map(lambda c: c['Key'].split('/')[-1], checkpoints))

        # Skip training session if no checkpoints are found
        if not checkpoint_names:
            print('No checkpoints found. Skipping this training session.')
            print(f'Waiting {frequency_hours}h until next training session...')
            time.sleep(frequency_seconds)
            continue

        # Continue with FedAvg process
        print(f'Found {len(checkpoint_names)} checkpoints in this training session. Starting FedAvg process.')

        # Download checkpoints from S3 bucket...
        tmp_path = f"/tmp/{subfolder}"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        for checkpoint in checkpoints:
            checkpoint_path = checkpoint['Key']
            file_name = checkpoint_path.split('/')[-1]
            print(f'Downloading {file_name} from S3 bucket.')
            s3_client.download_file(bucket_name, checkpoint_path, f"{tmp_path}/{file_name}")

        # Perform FedAvg...
        first_checkpoint = f"{tmp_path}/{checkpoint_names[0]}"
        tensors = tf.train.list_variables(first_checkpoint)

        agg_tensors = []
        for tensor in tensors:
            name = tensor[0]
            dtype = tf.float32
            agg_value = None
            print(f'Tensor name={name}, dtype={dtype}')
            for checkpoint in checkpoint_names:
                checkpoint_path = f"{tmp_path}/{checkpoint}"
                value = tf.raw_ops.Restore(
                    file_pattern=checkpoint_path,
                    tensor_name=name,
                    dt=dtype
                )
                agg_value = value if agg_value is None else agg_value + value

            agg_value = agg_value / len(checkpoint_names)
            agg_tensors.append((name, agg_value))

        # Save aggregated checkpoint...
        agg_checkpoint = f"{tmp_path}/agg_checkpoint.ckpt"
        tf.raw_ops.Save(
            filename=agg_checkpoint,
            tensor_names=[tensor[0] for tensor in agg_tensors],
            data=[tensor[1] for tensor in agg_tensors]
        )

        print(f'Finished FedAvg process. Uploading agg_checkpoint.ckpt to S3 bucket.')

        s3_client.upload_file(Filename=agg_checkpoint, Bucket=bucket_name, Key=f'server_checkpoints/{train_session_id}/agg_checkpoint.ckpt')

        # Remove tmp directory
        os.system(f"rm -r {tmp_path}")

        print('Sending download notification to clients.')
        requests.get(f'{endpoint}/send_checkpoint/{train_session_id}')

        print(f'Finished training session with id={train_session_id}.')
        print(f'Waiting {frequency_hours}h until next training session...')

        time.sleep(frequency_seconds)
