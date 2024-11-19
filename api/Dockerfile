FROM python:3.9-slim

WORKDIR /app/api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/api
COPY ./tests /app/tests

ENV PYTHONPATH=/app

EXPOSE ${PORT}

#CMD ["sh", "-c", "cd api && flask db upgrade && flask run --host=0.0.0.0"]
CMD ["sh", "-c", "flask db upgrade && python app.py"]