#!/bin/bash
set -e
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

rm -rf /opt/Webhook
git clone https://github.com/tgbot-collection/Webhook /opt/
pip3 install tornado

cp dockerhub.service /lib/systemd/system/

systemctl daemon-reload
systemctl enable dockerhub
systemctl start dockerhub

if [ $? == 0 ]
then
   echo "success"
else
   echo "fail"
fi