#!/bin/bash
sudo ln -sf $(pwd)/nginx/nginx.conf /etc/nginx/sites-available/f0kes.xyz
sudo ln -sf /etc/nginx/sites-available/f0kes.xyz /etc/nginx/sites-enabled/f0kes.xyz
sudo systemctl reload nginx
sudo systemctl enable nginx