# Configure base OS
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 1

# Install psql
RUN apt-get update -qq \
    && apt-get install -y postgresql-client

# Working directory
WORKDIR /drf_carapi

# Install dependencies
COPY requirements.txt /drf_carapi/requirements.txt
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /drf_carapi/requirements.txt

# Copy project to container
COPY . /drf_carapi/