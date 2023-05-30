#!/bin/bash

#echo "works"
cd [path_to_folder]/rss
. env/bin/activate
python3 [path_to_folder]/rss/rssfeed.py > /dev/null 2>&1
