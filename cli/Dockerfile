FROM python:3.9-slim

WORKDIR /cli

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /cli

ENV API_URL=https://web:5000/tarefas
ENV CERT_PATH=/cli/ssl/server.crt