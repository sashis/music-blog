#!/bin/bash

set -e

cp nginx.conf /etc/nginx/nginx.conf
cp supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ln -sf /dev/stdout /var/log/nginx/access.log
ln -sf /dev/stderr /var/log/nginx/error.log

echo "Upgrading db schema..."
while ! music_blog db upgrade
do
    echo "Retry db schema upgrading..."
    sleep 5
done

if [ "$MUSIC_BLOG_DEMO" == 'yes' ]; then
  echo "Initiating demo data..."
  music_blog demo
fi

exec /usr/bin/supervisord
