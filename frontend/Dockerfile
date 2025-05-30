# Stage 1: Build Angular app
FROM node:18 AS builder
WORKDIR /app

COPY app_frontend/package*.json ./
RUN npm install

COPY app_frontend/ ./
RUN npx ng build --configuration=production

# Stage 2: Serve with Nginx
FROM nginx:alpine

RUN rm -rf /etc/nginx/conf.d/*
COPY default.conf /etc/nginx/conf.d/default.conf
#RUN ls -l /app/dist/app_frontend
COPY --from=builder /app/dist/app_frontend/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
