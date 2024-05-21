#!/bin/bash

python src/main.py
if [ $? -ne 0 ]; then
    echo "Something went wrong with generating the server's files."
    exit 1
else
    python server.py --dir public
fi