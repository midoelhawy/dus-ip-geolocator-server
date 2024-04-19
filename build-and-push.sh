#!/bin/bash

latest_tag=$(git describe --tags --abbrev=0)

sudo docker build -t midoelhawy/dus-ip-geolocator-server:$latest_tag -t midoelhawy/dus-ip-geolocator-server:latest . --push