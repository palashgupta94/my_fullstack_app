#!/bin/bash

# Deployment Script for Fullstack Application

# Configuration
DOCKER_USERNAME="palashgupta94"  # Your Docker Hub username
FRONTEND_IMAGE="frontend-app"
BACKEND_IMAGE="backend-app"
VERSION="1.0"
GITHUB_REPO="https://github.com/palashgupta94/my_fullstack_app.git"
COMMIT_MESSAGE="Initial commit"

# Validate Docker username
if [[ "$DOCKER_USERNAME" == *"@"* ]]; then
  echo "ERROR: Docker username cannot contain @ symbols. Use your Docker Hub username, not email."
  exit 1
fi

# Function to handle errors
handle_error() {
  echo "Error: $1"
  exit 1
}

# Part 1: Docker Operations
echo "=== Starting Docker Build & Push ==="

echo "Building frontend image..."
docker build -t $DOCKER_USERNAME/$FRONTEND_IMAGE:$VERSION ./frontend/app_frontend || handle_error "Failed to build frontend image"

echo "Building backend image..."
docker build -t $DOCKER_USERNAME/$BACKEND_IMAGE:$VERSION ./backend || handle_error "Failed to build backend image"

echo "Pushing images to Docker Hub..."
docker push $DOCKER_USERNAME/$FRONTEND_IMAGE:$VERSION || handle_error "Failed to push frontend image"
docker push $DOCKER_USERNAME/$BACKEND_IMAGE:$VERSION || handle_error "Failed to push backend image"

