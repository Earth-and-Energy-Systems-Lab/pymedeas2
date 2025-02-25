# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# to avoid ImportError: libtk8.6.so: cannot open shared object file
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set up the volume
VOLUME /app/outputs

#RUN mkdir -p /app/outputs && chmod -R 777 /app/outputs

# Ensure the directory has write permissions
RUN chmod -R 777 /app/models/pymedeas_w/

ENTRYPOINT [ "python", "/app/run.py" ]
