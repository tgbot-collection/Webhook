#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

cd /home/benny/YYeTsBot
git pull

docker build -t bennythink/yyetsbot:arm64 .
docker push bennythink/yyetsbot:arm64