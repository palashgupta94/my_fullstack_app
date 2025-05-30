# My Fullstack App 🚀

A full-stack web application with:

- Flask backend (Python)
- Angular frontend
- Docker support
- MongoDB integration with fallback mechanism
- NGINX for frontend deployment

---

## ✅ Prerequisites

Before running the app, make sure the following are installed:

- **Docker** (**Mandatory**)
- **Node.js**(Optional. Only to run application locally)
- **Angular CLI**(Optional. Only to run application locally)
- **Python 3.9+** (optional, if running backend outside Docker)
- **MongoDB** (optional, needed only if testing with a local MongoDB instance)

---

## ✅ Features

- Supports all 4 CRUD operations (backend)
- Frontend supports POST operation only
- MongoDB support (local/Atlas)
- JSON fallback support when MongoDB is down or unavailable

---

## ✅ Running with Local MongoDB (Dockerised)

> Use this method to test locally using a Docker MongoDB instance.

### Step 1: Create Docker Bridge Network

```bash
docker network create my_fullstack_app_app-network
```

### Step 2: Run MongoDB Container

```bash
docker run --network=my_fullstack_app_app-network --name mymongo mongo:latest
```

### Step 3: Use `app-local-docker-compose.yml` to run the app

```bash
docker compose -f app-local-docker-compose.yml up --build
```

> Make sure all services (backend, frontend, mongo) are on the same network (`my_fullstack_app_app-network`).

---

## ✅ Running with MongoDB Atlas

If you want to connect the backend to a MongoDB Atlas cluster, use the following steps:

### Step 1: Update the `.env` file in the root of the project (`my_fullstack_app/`)

```env
MONGODB_ATLAS_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster
MONGODB_DB_NAME=mydatabase
MONGODB_COLLECTION_NAME=mycollection
```

> Make sure this `.env` file is present in the root directory.

### Step 2: Run the app with:

```bash
docker compose -f app-docker-compose.yml up --build
```

---

## ✅ Running on Bare Metal (Local System)

If you don't want to use Docker, then:

- Install Node, Angular CLI, Python (Flask), and dependencies
- MongoDB is optional (fallback JSON will be used if MongoDB is not running)
- Run backend: `python app.py`
- Run frontend: `ng serve` or build and serve via NGINX

---

## ✅ Fallback Mechanism

- If MongoDB is not available, the backend will fallback to `fallback_data.json` located at:

```
/backend/data/fallback_data.json
```

---

## ✅ NGINX Configuration (Frontend)

The Angular frontend is served via NGINX using the following configuration:

📄 **`frontend/default.conf`**

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

This ensures Angular routing works properly with Docker and NGINX.

---

## ✅ Useful Links

- 🔗 **GitHub Repository**: [Your GitHub Link Here]
- 🐳 **DockerHub Images**:
  - Backend: [DockerHub backend image link]
  - Frontend: [DockerHub frontend image link]

---

## ✅ Environment Variables Reference

`.env` file required in root folder (inside `my_fullstack_app/`):

```env
MONGODB_ATLAS_URI=mongodb://mymongo:27017   # or use Atlas URI
MONGODB_DB_NAME=mydatabase
MONGODB_COLLECTION_NAME=mycollection
JSON_FALLBACK_PATH=/data/fallback_data.json
```

---

Happy Devving! 💻🔥
