#!/bin/bash
cd /opt/Star-burger || exit 1
echo $(git pull) || exit 1
echo $(. ./env/bin/activate) || exit 1

echo $(pip install -r requirements.txt) || exit 1
echo $(apt install -y nodejs) || exit 1
echo $(apt install -y npm) || exit 1
echo $(./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./") || exit 1

echo $(python manage.py collectstatic --noinput) || exit 1
echo $(python manage.py migrate) || exit 1
echo $(systemctl restart burger_backend.service) || exit 1
echo $(systemctl reload nginx.service) || exit 1

last_commit=$(git rev-parse HEAD)
echo $(curl -H "X-Rollbar-Access-Token: 0b5d8ca7d05548969b1611c26e7a4767" \
          -H "Content-Type: application/json" \
          -X POST 'https://api.rollbar.com/api/1/deploy' \
          -d '{"environment": "production", "revision": "'${last_commit}'", "rollbar_name": "starburger", "local_username": "Norgius", "status": "succeeded"}')
echo Deploy was successful