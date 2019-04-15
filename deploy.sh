#!/bin/bash

cp ./norns.py /usr/local/bin/norns
chmod +x /usr/local/bin/norns

cp ./rsync_excludes.txt ~/.norns_excludes
cp ./norns.ini ~/.norns.ini
