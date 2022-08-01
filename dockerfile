# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

workdir /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT=8080
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["python", "run.py"]
