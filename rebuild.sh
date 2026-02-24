#!/usr/bin/env bash

sudo docker compose down
start_dir=$(pwd)

find . -type d | while read dir; do
    if [ -d "$dir/.git" ]; then
        echo "Updating $dir"
        (cd "$dir" && git pull)
        cd "$start_dir"
    fi
done

sudo nginx -t && sudo systemctl reload nginx
sudo systemctl enable nginx

sudo docker compose up --build -d
