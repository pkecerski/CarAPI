# Configure OS
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

# Working directory
WORKDIR /drf_carapi

# Install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Install dependencies
COPY requirements.txt /drf_carapi/requirements.txt
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /drf_carapi/requirements.txt

# Copy project to container
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# Add and run as non-root user
RUN adduser -D myuser
USER myuser

# Run gunicorn
CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT