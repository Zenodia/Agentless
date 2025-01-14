# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --assume-yes git


# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY . /workspace/
COPY requirements.txt /workspace
# Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /workspace 
# Install the package
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyterlab 

#COPY server.py /app/server.py

# Expose the port your server will run on
EXPOSE 65432

#CMD ["python", "/app/server.py"]
