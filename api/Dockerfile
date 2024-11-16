FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/api
COPY ./tests /app/tests

EXPOSE 5000

CMD ["sh", "-c", "cd api && flask db upgrade && flask run --host=0.0.0.0"]