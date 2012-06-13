#!/bin/bash

KEY_LOC=`pwd`/../keys/zoufkey.pem
DEPLOY_SERVER=ubuntu@ec2-50-17-101-100.compute-1.amazonaws.com

CMD="cd ~/deploy"
CMD=$CMD" && git pull"
CMD=$CMD" && python manage.py collectstatic --noinput"
CMD=$CMD" && sudo apachectl restart"

echo "Running"
echo $CMD

echo "---"
ssh -i $KEY_LOC $DEPLOY_SERVER $CMD
