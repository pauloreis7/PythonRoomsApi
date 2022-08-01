# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

workdir /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main.config.http_server_configs:app", "--host", "0.0.0.0", "--port", "8080"]
