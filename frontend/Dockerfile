# Stage 1: Build
FROM node:22-alpine as builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --quiet

COPY . .
RUN npm run build -- --configuration=production

# Stage 2: Serve
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy build files
COPY --from=builder /app/dist/frontend /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
