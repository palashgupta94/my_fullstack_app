
# My Fullstack App (Kubernetes Ready ✅)


A full-stack web application built with:

- ✅ Flask backend (Python)
- ✅ Angular frontend
- ✅ MongoDB (Local or Atlas) with fallback to JSON
- ✅ Docker and Kubernetes deployment support
- ✅ NGINX for frontend routing

---

## Table Of Contents

- [Prerequisites](#prerequisites)
- [Features](#features)
- [Running With Kubernetes](#running-with-kubernetes)
- [Running With Docker (Local MongoDB)](#running-with-local-mongodb-dockerised)
- [Running With MongoDB Atlas](#running-with-mongodb-atlas)
- [Running On Local System (Baremetal)](#running-on-bare-metal-local-system)
- [Fallback Mechanism & Mongo Sync Logic](#fallback-mechanism--mongo-sync-logic)
- [NGINX Frontend Configuration](#nginx-frontend-configuration)
- [Environment Variables Reference](#environment-variables-reference)
- [Useful Links](#useful-links)

---

## 🧩 Features

- 🔁 Full CRUD support via Flask backend
- 🧾 JSON fallback when MongoDB is down
- 🎯 Angular frontend with form support
- 📦 Docker and Kubernetes ready
- 🌐 NGINX static hosting and reverse proxy

---

## 🧵 Fallback Mechanism & Mongo Sync Logic

### 🔄 Automatic Fallback to JSON

If MongoDB is **down/unreachable**, the backend will automatically:

- Read and write data to `fallback_data.json`
- Continue serving and storing user data
- Log all fallback events

Fallback file path (can be customized):

```
/data/fallback_data.json
```

### 🧠 MongoDB Auto-Reconnection

- A background thread continuously **monitors MongoDB**.
- Tries to reconnect every 10 seconds when down.

### 🔁 Sync Fallback to MongoDB

- Another background thread syncs all fallback items from JSON to MongoDB.
- Runs every 30 seconds.
- Avoids duplicates using the `id` field.

### 🔐 Thread-safe File Access

- All file operations are wrapped using a `threading.Lock` to prevent race conditions.

---

## 🚀 Running With Kubernetes

### 1. Start Minikube (or kind)

```bash
minikube start --driver=docker
```

### 2. Apply Kubernetes YAMLs

```bash
kubectl apply -f k8s/configmap-app-config.yaml
kubectl apply -f k8s/configmap-nginx.yaml
kubectl apply -f k8s/deployment-mongo.yaml
kubectl apply -f k8s/deployment-backend.yaml
kubectl apply -f k8s/deployment-frontend.yaml
kubectl apply -f k8s/ingress.yaml
```

### 3. Enable Ingress (Minikube only)

```bash
minikube addons enable ingress
```

### 4. Add Local DNS Entry

Edit `/etc/hosts`:

```bash
127.0.0.1 myapp.local
```

### 5. Visit Application

Open [http://myapp.local](http://myapp.local) in your browser.

---

## 🐋 Running With Local MongoDB (Dockerised)

```bash
docker network create my_fullstack_app_app-network

docker run --network=my_fullstack_app_app-network --name mymongo mongo:latest

docker compose -f app-local-docker-compose.yml up --build
```

---

## ☁️ Running With MongoDB Atlas

Update `.env`:

```env
MONGODB_ATLAS_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=mydatabase
MONGODB_COLLECTION_NAME=mycollection
```

Run:

```bash
docker compose -f app-docker-compose.yml up --build
```

---

## 🖥️ Running On Local System (Baremetal)

1. Install Python 3.9+, Flask, Node.js, and Angular CLI
2. Set up `.env` with Mongo URI or leave Mongo off to use fallback
3. Start backend:

```bash
python app.py
```

4. Start frontend:

```bash
ng serve
```

---

## 🌐 NGINX Frontend Configuration

Used in both Docker and Kubernetes:

```nginx
server {
  listen 80;
  server_name localhost;

  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
  }

  location /api {
    proxy_pass http://backend:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

---

## 🌱 Environment Variables Reference

Used via `.env` (for Docker) or ConfigMap (Kubernetes):

```env
MONGODB_ATLAS_URI=mongodb://mongo:27017  # or your Atlas URI
MONGODB_DB_NAME=mydatabase
MONGODB_COLLECTION_NAME=mycollection
JSON_FALLBACK_PATH=/data/fallback_data.json  # Optional
```

---

## 🔗 Useful Links

- GitHub: [https://github.com/palashgupta94/my_fullstack_app](https://github.com/palashgupta94/my_fullstack_app)
- DockerHub:
  - Backend: `docker pull palashgupta94/backend:v1.0.0`
  - Frontend: `docker pull palashgupta94/frontend:v1.0.0`

---

✅ Happy Cloud-Native Hacking!
v