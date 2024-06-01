# Dockerfile
FROM python:3.9-slim-buster
 
# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD exec gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 app:app

