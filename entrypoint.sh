#!/bin/bash
python3.6 bot.py > bot-log.txt 2>&1 &
nodejs foobar.js > node-log.txt 2>&1 &

for job in $(jobs -p); do
    echo Waiting for ${job} to terminate.
    wait ${job}
done