# # backend/Dockerfile
# FROM python:3.12

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --upgrade pip && apt-get install -y ca-certificates && pip install --no-cache-dir -r requirements.txt

# # Install CA certificates
# RUN apt-get update && apt-get install -y ca-certificates

# COPY . .

# CMD ["python", "app.py"]

# backend/Dockerfile
FROM python:3.12

WORKDIR /app

# Install dependencies and tools
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y vim ca-certificates bash && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "alias ll='ls -lrth'" >> ~/.bashrc

# Copy application code
COPY . .

# Start the app
CMD ["python", "app.py"]
