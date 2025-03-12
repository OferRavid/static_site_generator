#!/bin/bash

python src/main.py
if [ $? -ne 0 ]; then
    echo "Something went wrong with generating the server's files."
    exit 1
else
    cd public && python3 -m http.server 8888
fi