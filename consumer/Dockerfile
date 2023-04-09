FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the consumer script to the working directory
COPY consumer.py .

# Start the consumer script when the container starts
CMD ["python", "consumer.py"]