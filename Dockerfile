FROM python:3.10-slim AS backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 
COPY . .


FROM node:14-alpine AS frontend

WORKDIR /app
COPY bundles-src bundles-src
COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm ci --dev
CMD ["./node_modules/.bin/parcel", "build", "bundles-src/index.js", "--dist-dir", "bundles", "--public-url", "./"]


FROM nginx:latest AS nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY docker_production/nginx.conf /etc/nginx/conf.d
COPY docker_production/proxy_params /etc/nginx
