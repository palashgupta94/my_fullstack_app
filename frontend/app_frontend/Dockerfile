## Development Dockerfile for Angular (frontend/app_frontend/Dockerfile.dev)
#FROM node:22-alpine
#
#WORKDIR /app
#
## Copy package files first for better caching
#COPY package.json package-lock.json ./
#
## Install dependencies (include dev dependencies)
#RUN npm install
#
## Copy all files (except those in .dockerignore)
#COPY . .
#
## Expose ports
#EXPOSE 4200 49153
#
## Start development server with hot-reload
#CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--poll", "1000"]


# Development Dockerfile for Angular (frontend/app_frontend/Dockerfile.dev)
# Development Dockerfile for Angular (frontend/app_frontend/Dockerfile.dev)
FROM node:22-alpine

WORKDIR /app

# 1. Update npm first
RUN npm install -g npm@latest

# 2. Copy package files
COPY package.json package-lock.json ./

# 3. Fix package-lock.json if needed
RUN npm install --package-lock-only && \
    npm audit fix --package-lock-only

# 4. Clean install
RUN npm ci --audit --fund

# 5. Copy application code
COPY . .

EXPOSE 4200
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--poll", "1000"]
