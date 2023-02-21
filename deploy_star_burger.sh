#!/bin/bash

set -e
cd /opt/Star-burger
git pull
. ./env/bin/activate

pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

python manage.py collectstatic --noinput
python manage.py migrate --noinput

systemctl restart burger_backend.service
systemctl reload nginx.service

last_commit=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: 0b5d8ca7d05548969b1611c26e7a4767" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d '{"environment": "production", "revision": "'${last_commit}'", "rollbar_name": "starburger", "local_username": "Norgius", "status": "succeeded"}'
echo Deploy was successful