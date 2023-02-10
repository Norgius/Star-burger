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

echo Deploy was successful