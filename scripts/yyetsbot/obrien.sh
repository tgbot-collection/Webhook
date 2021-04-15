#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

docker pull bennythink/yyetsbot
docker-compose -f/root/BotsRunner/docker-compose.yml up -d yyets
#docker system prune -a --volumes -f