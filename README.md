### Tapway Publish / Subscribe with RabbitMQ


#### Requirements
- One webservice to publish data
- RabbitMQ based broker
- Consumer client
- Testing up to 1000 requests


#### Steps

##### Start clusters
- Make sure docker is running: `docker info`
- On Linux or WSL: `sh 01_start.sh` to start docker compose cluster

##### Test by 1000 requests
- Go to tests folder: `cd tests`
- Create python virtual environment (assuming testing using virtualenv): `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install necessary requirements: `pip install -r requirements.txt`
- Run test script (script is modifiable): `python thousand_requests.py`
- OUTPUT FILE will be available at `consumer/output/output.csv`

##### Remove containers, network, volumes, images
- On Linux or WSL: `sh 02_down.sh` to shutdown docker compose cluster and remove artifacts
- Remove csv output (optional): `sudo rm -rf consumer/output/output.csv`


#### Summary
- Project consists of 3 main services reflected by file structures:
    - producer: fastapi based web service with POST endpoint according to specification:
        ```
        {
            "device_id": str,
            "client_id": str,
            "created_at": str, # timestamp, e.g. '2023-02-07 14:56:49.386042'
            "data": {
                "license_id": str,
                "preds": [
                    {
                        "image_frame": str, # base64 string
                        "prob": float,
                        "tags": str[]
                    },
                    ...
                ] 
            }
        }
        ```
    
    - broker: RabbitMQ as AMQP service with minimal customization

    - consumer: Client based on python `pika` package (to subscribe from broker), and to trandform and load data to CSV.

- tests folder is to house testing environment

- bash scripts is to facilitate clusters management