#!/bin/bash

./scripts/download-latest-mmdb.sh
echo "Current version of db is:"
cat current_db_version.txt 
python3 main.py
