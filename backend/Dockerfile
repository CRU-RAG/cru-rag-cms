# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory within the container
WORKDIR /versewise-cms-backend

# Copy the necessary files and directories into the container
COPY app/ config.py .env run.py requirements.txt /versewise-cms-backend/
COPY app/ /versewise-cms-backend/app/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["python3", "run.py"]