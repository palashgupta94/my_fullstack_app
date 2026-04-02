# My Fullstack App (Kubernetes and AWS Ready)


A full-stack web application built with:

- Flask backend (Python)
- Angular frontend
- MongoDB (Local or Atlas) with fallback to JSON
- Docker and Kubernetes deployment support
- NGINX for frontend routing

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
- [AWS Support](#aws-amazon-web-services-deployment)
- [Useful Links](#useful-links)

---

## Features

- Full CRUD support via Flask backend
- JSON fallback when MongoDB is down
- Angular frontend with form support
- Docker and Kubernetes ready
- NGINX static hosting and reverse proxy

---

## Fallback Mechanism & Mongo Sync Logic

### Automatic Fallback to JSON

If MongoDB is **down/unreachable**, the backend will automatically:

- Read and write data to `fallback_data.json`
- Continue serving and storing user data
- Log all fallback events

Fallback file path (can be customized):

```
/data/fallback_data.json
```

### MongoDB Auto-Reconnection

- A background thread continuously **monitors MongoDB**.
- Tries to reconnect every 10 seconds when down.

### Sync Fallback to MongoDB

- Another background thread syncs all fallback items from JSON to MongoDB.
- Runs every 30 seconds.
- Avoids duplicates using the `id` field.

### Thread-safe File Access

- All file operations are wrapped using a `threading.Lock` to prevent race conditions.

---

## Running With Kubernetes

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

## Running With Local MongoDB (Dockerised)

```bash
docker network create my_fullstack_app_app-network

docker run --network=my_fullstack_app_app-network --name mymongo mongo:latest

docker compose -f app-local-docker-compose.yml up --build
```

---

## Running With MongoDB Atlas

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

## Running On Local System (Baremetal)

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

## NGINX Frontend Configuration

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

## Environment Variables Reference

Used via `.env` (for Docker) or ConfigMap (Kubernetes):

```env
MONGODB_ATLAS_URI=mongodb://mongo:27017  # or your Atlas URI
MONGODB_DB_NAME=mydatabase
MONGODB_COLLECTION_NAME=mycollection
JSON_FALLBACK_PATH=/data/fallback_data.json  # Optional
```

---

## AWS (Amazon Web Services) Deployment

### 1. Deploy Backend and Frontend on single EC2 Instance
1. Launch an **EC2 instance** (Ubuntu 22.04 recommended).
2. Connect to EC2 using SSH:

```bash
ssh -i mykey.pem ubuntu@<EC2_PUBLIC_IP>
```
3. Update packages:
```bash
sudo apt update && sudo apt upgrade -y
```

4. Install dependencies:
```bash
sudo apt install -y python3 python3-pip nodejs npm nginx git
```

5. Clone your repository:
```bash
git clone https://github.com/username/my_fullstack_app.git
cd my_fullstack_app
```

6. Setup backend (Flask):
```bash
cd backend
pip3 install -r requirements.txt
nohup python3 app.py --host=0.0.0.0 --port=5000 &
```
7. Build frontend (Angular/Express):
```bash
cd ../frontend
npm install
npm run build
```

8. Configure Nginx to serve frontend and proxy `/api` to Flask:
```bash
sudo nano /etc/nginx/sites-available/myapp
```

Example:
```json
server {
  listen 80;
  server_name _;
  root /home/ubuntu/my_fullstack_app/frontend/dist;
  index index.html;

  location / {
    try_files $uri /index.html;
  }

  location /api {
    proxy_pass http://127.0.0.1:5000;
  }
}

```
9. Copy build files to Nginx web root
The default root is /var/www/html/ (it gets created after installing Nginx):
```bash
sudo rm -rf /var/www/html/*
sudo cp -r dist/your-project-name/* /var/www/html/
```

10. Restart Nginx
```bash
sudo systemctl restart nginx
```
11. Access the app via `http://<EC2_PUBLIC_IP>`.

---

### 2. Deploy Backend & Frontend in Separate EC2 Instances
- Flask backend
  1. Launch an EC2 instance for backend.
  2. SSH into instance and install Python:
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip git
  ```
  3. Clone repo and run Flask app:
  ```bash
  git clone https://github.com/username/my_fullstack_app.git
  cd my_fullstack_app/backend
  pip3 install -r requirements.txt
  nohup python3 app.py --host=0.0.0.0 --port=5000 &
  ```
  4. Ensure security group allows inbound traffic on port `5000`.
  ---
- Angular Frontend
  1. Launch another EC2 instance for frontend.
  
  2. SSH into instance and install Node.js + Nginx:
  ```bash
  sudo apt update && sudo apt install -y nodejs npm nginx git
  ```
  
  3. Clone repo and build frontend:
  ```bash
  git clone https://github.com/username/my_fullstack_app.git
  cd my_fullstack_app/frontend
  npm install
  npm run build
  ```
  
  4. Configure Nginx to serve frontend and forward API requests to **backend’s private IP or EC2 public DNS**
  ```json
  location /api {
    proxy_pass http://<BACKEND_EC2_PRIVATE_IP>:5000;
  }
  ```
  
  5. Copy build files to Nginx web root
  The default root is /var/www/html/ (it gets created after installing Nginx):
  ```bash
    sudo rm -rf /var/www/html/*
    sudo cp -r dist/your-project-name/* /var/www/html/
  ```
  
  6. Restart Nginx
  ```bash
  sudo systemctl restart nginx
  ```
  
  7. Access the frontend via `http://<FRONTEND_EC2_PUBLIC_IP>`
  
---
### 3. Deploy Backend & Frontend Using **Docker + ECR + ECS + VPC**
1. Build Docker Image
```bash
# Backend
cd backend
docker build -t my-backend -f Aws_Dockerfile .

# Frontend
cd ../frontend
docker build -t my-frontend -f Aws_Dockerfile .
```
2. Push Images to Amazon ECR
    
    1. Create ECR repositories:
    ```bash
    aws ecr create-repository --repository-name my-backend
    aws ecr create-repository --repository-name my-frontend
    ```

    2. Authenticate Docker with ECR:
    ```bash
    aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.ap-south-1.amazonaws.com
    ```

    3. Tag & push images:
    ```bash
    docker tag my-backend:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/my-backend:latest
    docker tag my-frontend:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/my-frontend:latest

    docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/my-backend:latest
    docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/my-frontend:latest
    ```

  3. Create ECS Cluster
    - Go to ECS console → Create cluster → Select VPC + Subnets.

  4. Define Task Definitions
      - One for backend (Flask).

      - One for frontend (Angular/Express).

      - Set container ports `(5000 for backend, 80 for frontend)`.

  5. Create ECS Service
      - Create a service for backend.

      - Create a service for frontend.

      - Attach services to Application Load Balancer (ALB) or Cloud Map.

  6. Update Frontend Env Var

      - Set `BACKEND_URL` in frontend in Frontend Nginx.conf → `backend.myapp.local:5000` or `<Backend IP>:5000` (Cloud Map).

  Example
  ```json
    Server {
    listen 80;
    server_name localhost;

    location / {
      root /usr/share/nginx/html;
      index index.html index.htm;
      try_files $uri $uri/ /index.html;
    }

    location /api {
      proxy_pass http://$BACKEND_URL;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
  ```

  7. Verify With Frontend Public IP.
      - `http://<Frontend public IP>`.
      If doesn't work go to ECS Console -> Cluster & Service -> Select Frontend Service -> Task Details -> Click on task details of running task ->Copy Security Group Id -> Go to EC2 Console -> Security Groups -> Select Group (paste copied id in search bar) -> Inbound Group -> validate port 80 -> If not -> Edit Inbound Rules -> Add Rule -> Type Http (port 80 will get select by default) -> Source 0.0.0.0/0 -> save rule. ->  try again 

---

## Useful Links

- GitHub: [https://github.com/palashgupta94/my_fullstack_app](https://github.com/palashgupta94/my_fullstack_app)
- DockerHub:
  - Backend: `docker pull palashgupta94/backend:v1.0.0`
  - Frontend: `docker pull palashgupta94/frontend:v1.0.0`

---

Happy Cloud-Native Hacking!

---

## Terraform Deployment (AWS)

Three deployment configurations using Terraform and AWS.

### Prerequisites

- Terraform >= 1.5 installed
- AWS CLI configured (`aws configure`)
- EC2 Key Pair created in AWS Console
- S3 bucket for Terraform state

### Create S3 State Bucket (Run Once)
```bash
aws s3api create-bucket \
  --bucket my-terraform-state-bucket \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1

aws s3api put-bucket-versioning \
  --bucket my-terraform-state-bucket \
  --versioning-configuration Status=Enabled
```

---

### Part 1 — Single EC2 Instance (Flask + Angular)

Both Flask (port 5000) and Angular (port 80 via Nginx) run on a single EC2 instance.

**Architecture:**
```
Internet → EC2 (Public IP)
              ├── Flask  :5000  (systemd service)
              └── Nginx  :80    (serves Angular, proxies /api to Flask)
```

**Deploy:**
```bash
cd part1
terraform init
terraform plan  -var="key_name=YOUR_KEY_PAIR"
terraform apply -var="key_name=YOUR_KEY_PAIR"
```

**Access:**
```bash
terraform output app_url    # Angular frontend
terraform output flask_url  # Flask backend
```

---

### Part 2 — Separate EC2 Instances

Flask and Angular run on two separate EC2 instances inside a custom VPC.

**Architecture:**
```
Internet
  ├── Angular EC2 (Public IP) :80   → Flask EC2 (Private IP) :5000
  └── Flask EC2   (Public IP) :5000
```

**Deploy:**
```bash
cd part2
terraform init
terraform plan  -var="key_name=YOUR_KEY_PAIR"
terraform apply -var="key_name=YOUR_KEY_PAIR"
```

**Access:**
```bash
terraform output angular_url   # Angular frontend
terraform output flask_url     # Flask backend
```

---

### Part 3 — Docker + ECR + ECS + ALB

Both apps run as Docker containers on ECS Fargate with ALB path-based routing.

**Architecture:**
```
Internet → ALB (port 80)
              ├── /api/* → ECS Flask Service  (Fargate, port 5000)
              └── /*     → ECS Angular Service (Fargate, port 80)
```

**Step 1 — Create ECR repos:**
```bash
cd part3
terraform init
terraform apply \
  -target=aws_ecr_repository.backend \
  -target=aws_ecr_repository.frontend
```

**Step 2 — Build and push Docker images:**
```bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=ap-south-1

aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com

# Backend
cd backend
docker build -t my-backend -f Aws_Dockerfile .
docker tag my-backend:latest \
  $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/my-backend:latest
docker push \
  $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/my-backend:latest

# Frontend
cd ../frontend
docker build -t my-frontend -f Aws_Dockerfile .
docker tag my-frontend:latest \
  $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/my-frontend:latest
docker push \
  $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/my-frontend:latest
```

**Step 3 — Deploy full infrastructure:**
```bash
cd part3
terraform apply
terraform output alb_dns_name
```

**Access:**
```bash
terraform output app_url  # Angular via ALB
terraform output api_url  # Flask via ALB
```

---

### Destroy Resources (Avoid AWS Charges)
```bash
cd part1 && terraform destroy -var="key_name=YOUR_KEY_PAIR"
cd part2 && terraform destroy -var="key_name=YOUR_KEY_PAIR"
cd part3 && terraform destroy
```

---

## Folder Structure
```
my_fullstack_app/
├── backend/              # Flask Python app
├── frontend/             # Angular app
├── k8s/                  # Kubernetes manifests
├── part1/                # Terraform: Single EC2
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── user_data.sh
├── part2/                # Terraform: Separate EC2s
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── flask_user_data.sh
│   └── angular_user_data.sh
├── part3/                # Terraform: Docker + ECS + ALB
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── app-docker-compose.yml
├── app-local-docker-compose.yml
└── README.md
```
