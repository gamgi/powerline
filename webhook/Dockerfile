# Requires full python install for eventlet
FROM python:3.6-alpine
ADD . /webhook
WORKDIR /webhook
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "webhook.py"]
