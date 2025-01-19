# Base image
FROM python:3.9-slim

# Install system dependencies required for pyarrow
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsnappy-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install pandas pyarrow

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY pipeline.py pipeline.py

# Command to run the application
ENTRYPOINT ["python", "pipeline.py"]
