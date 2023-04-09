import pika
import json
from datetime import datetime

from fastapi import FastAPI, HTTPException, Body

app = FastAPI()

# Define the RabbitMQ connection parameters
rabbitmq_host = 'rabbitmq'
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'
rabbitmq_queue = 'image_queue'

def validate_request(request_data):
    required_fields = ['device_id', 'client_id', 'created_at', 'data']
    required_data_fields = ['license_id', 'preds']

    # Check that all required fields are present
    for field in required_fields:
        if field not in request_data:
            return False

    # Check that all required data fields are present
    for field in required_data_fields:
        if field not in request_data['data']:
            return False

    # Check that 'preds' is a list of dictionaries with the required fields
    for pred in request_data['data']['preds']:
        if not isinstance(pred, dict):
            return False
        if 'image_frame' not in pred or 'prob' not in pred or 'tags' not in pred:
            return False
        if not isinstance(pred['image_frame'], str) or not isinstance(pred['prob'], float) or not isinstance(pred['tags'], list):
            return False

    return True

@app.post("/")
async def handle_request(request_data: dict = Body(...)):
    if validate_request(request_data):
        # Add the 'low_prob' tag if necessary
        for pred in request_data['data']['preds']:
            if pred['prob'] < 0.25:
                pred['tags'].append('low_prob')

        # Add the current timestamp to the request
        request_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # Push the message to the RabbitMQ queue
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='image_queue')
        channel.basic_publish(exchange='', routing_key='image_queue', body=json.dumps(request_data))
        connection.close()

        return {'status': 'success'}
    else:
        raise HTTPException(status_code=400, detail='Invalid request data')