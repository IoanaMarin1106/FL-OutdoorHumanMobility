from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_cors import CORS
import os
import datetime
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Federated Learning Server', version='1.0.0')


# get AWS credentials
bucket_name = os.environ.get("BUCKET_NAME")
aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Get the environment variables
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')
socketio = SocketIO(app, logger=True, engineio_logger=True)


@socketio.on('initial_connect')
def initial_connect(message):
    current_socket_id = request.sid
    # send .tflite model file
    presigned_url = create_presigned_url(bucket_name, "models/mobility_model.tflite")
    socketio.emit('download_model', presigned_url, to=current_socket_id)
    print(f"New socket connection: {current_socket_id}")


@socketio.on('reconnect')
def reconnect(message):
    current_socket_id = request.sid
    # send latest checkpoint file
    print(f"Reconnection: {current_socket_id}")


@socketio.on('get_checkpoint_upload_url')
def get_checkpoint_upload_url(subfolder):
    sid = request.sid
    obj = f'clients_checkpoints/{subfolder}/checkpoint-{sid}.ckpt'
    response = create_presigned_upload_url(bucket_name, obj)
    socketio.emit('upload_checkpoint', response, to=sid)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='healthy'), 200

@app.route('/ping')
@metrics.gauge('in_progress', 'Ping requests in progress')
def ping():
    return "ok"


@app.route('/download_model')
def send_model():
    socketio.emit('download_model', "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg")
    return "model sent"


@app.route('/start_train')
def start_train():
    subfolder = create_checkpoints_subfolder()
    socketio.emit('start_train', subfolder)
    return subfolder


@app.route('/send_checkpoint/<subfolder>')
def send_checkpoint(subfolder):
    key = f'server_checkpoints/{subfolder}/agg_checkpoint.ckpt'
    url = create_presigned_url(bucket_name, key)
    socketio.emit("get_checkpoint", url)
    return "ok"


def create_checkpoints_subfolder() -> str:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H%M%S%f")
    return dt_string


def create_presigned_url(bucket, obj):
    try:
        key = obj
        s3_client = boto3.client(
            's3',
            region_name='eu-north-1',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url='https://s3.eu-north-1.amazonaws.com'
        )
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=600000
        )
    except ClientError as e:
        print(e)
        return None
    return url


def create_presigned_upload_url(bucket, obj,
                                fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client(
        's3',
        region_name='eu-north-1',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url='https://s3.eu-north-1.amazonaws.com'
    )
    try:
        response = s3_client.generate_presigned_post(bucket,
                                                     obj,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def upload_model(bucket_name, object_key, model_binary):
    client = boto3.client('s3')
    client.put_object(Body=model_binary, Bucket=bucket_name, Key=object_key)


if __name__ == '__main__':
    app.run()
