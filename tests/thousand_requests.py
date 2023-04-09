import requests
import json
import random
import string
import time

from datetime import datetime

# Define the endpoint URL
url = "http://localhost:8000/"

# Define the number of requests to send and the number of preds per request
num_requests = 1000
preds_per_request = 3

# Define the characters to use for generating random strings
characters = string.ascii_letters + string.digits

# Define a helper function to generate a random JSON body
def generate_json_body():
    # Generate random strings for the device ID and client ID
    device_id = ''.join(random.choices(characters, k=10))
    client_id = ''.join(random.choices(characters, k=10))

    # Generate a random timestamp string
    created_at = datetime.now().strftime("%Y%m%d_%H-%M-%S")

    # Generate random strings for the license ID, image frame, and tags
    license_id = ''.join(random.choices(characters, k=10))

    # Construct the JSON body
    json_body = {
        'device_id': device_id,
        'client_id': client_id,
        'created_at': created_at,
        'data': {
            'license_id': license_id,
            'preds': [
                {
                    'image_frame': ''.join(random.choices(characters, k=50)),
                    'prob': random.uniform(0, 1), # Generate a random probability value between 0 and 1
                    'tags': [''.join(random.choices(characters, k=5)) for i in range(3)]
                }
                for _ in range(preds_per_request)
            ]
        }
    }

    return json_body


for i in range(num_requests):
    # Generate a random JSON body
    json_body = generate_json_body()

    time.sleep(0.5)

    # Send the POST request to the producer endpoint
    response = requests.post(url, json=json_body)

    print(f'Request number: {i+1}, returning {response.status_code}')