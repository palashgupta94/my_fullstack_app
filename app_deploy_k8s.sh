#!/bin/bash

# Stop the script on the first error
set -e

echo "Starting Kubernetes deployment..."

echo "Applying MongoDB Deployment and Service..."
kubectl apply -f k8s/mongo-deployment.yaml

echo "Applying App ConfigMap (.env variables)..."
kubectl apply -f k8s/app-configmap.yaml

echo "Applying Backend Deployment and Service..."
kubectl apply -f k8s/backend-deployment.yaml

echo "Applying Frontend Deployment and Service..."
kubectl apply -f k8s/frontend-deployment.yaml

echo "Applying NGINX ConfigMap..."
kubectl apply -f k8s/nginx-configmap.yaml

echo "Applying Ingress Resource..."
kubectl apply -f k8s/ingress.yaml

echo "Deployment complete!"
