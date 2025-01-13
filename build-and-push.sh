#!/bin/bash
github_api_url="https://api.github.com/repos/midoelhawy/global-geo-ip-database-generator/releases/latest"
latest_version=$(curl -s $github_api_url | jq -r '.tag_name')
sudo docker build -t midoelhawy/dus-ip-geolocator-server:$latest_version -t midoelhawy/dus-ip-geolocator-server:latest . --push

echo "Docker image built and pushed successfully. Tags $latest_version; latest"