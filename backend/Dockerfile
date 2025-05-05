# backend/Dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && apt-get install -y ca-certificates && pip install --no-cache-dir -r requirements.txt

# Install CA certificates
RUN apt-get update && apt-get install -y ca-certificates

COPY . .

CMD ["python", "app.py"]

