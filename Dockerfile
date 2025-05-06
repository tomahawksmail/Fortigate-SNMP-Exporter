FROM python:3.11-slim

# Install required packages
RUN pip install --no-cache-dir paramiko prometheus_client pysnmp

# Copy the Python script into the container
COPY main.py /app/main.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "main.py"]