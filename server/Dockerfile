# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7.13-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update && \
    apt-get -y install curl \
    libpq-dev \
    gcc
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT