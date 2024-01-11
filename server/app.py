from flask import Flask, jsonify, request 
from dotenv import load_dotenv
from flask_cors import CORS
import os
import datetime
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the environment variables
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

def send_download_global_model_notification():
    download_global_model_url = "TODO"
    r = requests.post(download_global_model_url)

    if r.status_code != 200:
        print(f"Error:pip {r.status_code}")
    
    img_src = r.json()
    example = img_src["TODO"]
    print(example)


@app.route('/global_model', methods = ['GET'])
def hello():
    if (request.method == 'GET'):
        ct = datetime.datetime.now()
        model_update = [
                {
                    "timestamp": f"{ct}",
                    "data": "http://global-model1.com"
                }
            ]

        return model_update
    
if __name__ == '__main__':
    app.run()