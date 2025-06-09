# Use an official Python runtime as a base image
# Using a specific version (3.9) and a slim variant for smaller image size.
# 'slim-buster' is based on Debian Buster, providing a good balance of size and functionality.
FROM python:3.9-slim-buster

# Install wget which is used by your script to download the CSV file.
# apt-get update updates the package list, and apt-get install installs wget.
# rm -rf /var/lib/apt/lists/* cleans up apt cache to keep image size small.
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
# All subsequent instructions will be executed relative to this directory.
# This makes it easier to manage file paths within the container.
WORKDIR /app

# Copy the requirements.txt file into the container at the current WORKDIR (/app).
# This is done separately before copying the rest of the code to leverage Docker's caching.
# If requirements.txt doesn't change, this layer is reused, speeding up builds.
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt.
# --no-cache-dir: Prevents pip from storing cached files, reducing image size.
# -r: Specifies a requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory (where Dockerfile is located) into the container's WORKDIR (/app).
# This includes your ingest_data.py script.
COPY . .

# Define the default command to execute when the container starts.
# CMD is an array of strings representing the executable and its arguments.
# This makes the container "executable". It will run your Python script.
# We're providing placeholders for arguments here; actual values will be passed at runtime.
CMD ["python", "ingest_data.py", "--user", "root", "--password", "root", "--host", "localhost", "--port", "5432", "--db", "postgres", "--table_name", "yellow_taxi_data", "--url", "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"]
