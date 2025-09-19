FROM python:3.12-slim

RUN apt-get update && apt-get install -y chromium chromium-driver

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
