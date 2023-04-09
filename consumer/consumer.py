import os, sys
import pika
import csv
import json

from datetime import datetime

# Define the RabbitMQ connection parameters
rabbitmq_host = 'rabbitmq'
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'
rabbitmq_queue = 'image_queue'

output_file = f'output/output.csv'

def create_csv_header():

    with open(output_file, 'w', newline='') as csv_file:
        # Define the CSV headers
        csv_headers = ['device_id', 'client_id', 'created_at', 'license_id', 'image_frame', 'prob', 'tags']

        # Define the CSV writer and write the headers to the file
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_headers)

def main():
    # Define the RabbitMQ connection parameters and channel
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the RabbitMQ queue
    channel.queue_declare(queue=rabbitmq_queue)

    # # Define the CSV output file name
    # output_file = f'output/{datetime.now().strftime("%Y%m%d_%H:%M:%S")}.csv'

    # Define the RabbitMQ message consumer callback function
    def callback(ch, method, properties, body):
        
        # Parse the message JSON body
        message = json.loads(body)

        # Write each pred to a new CSV row
        with open(output_file, 'a', newline='') as csv_file:
            for pred in message['data']['preds']:
                row = [
                    message['device_id'],
                    message['client_id'],
                    message['created_at'],
                    message['data']['license_id'],
                    pred['image_frame'],
                    pred['prob'],
                    json.dumps(pred['tags'])
                ]
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consume messages from the RabbitMQ queue indefinitely
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        create_csv_header()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)