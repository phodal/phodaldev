#!/bin/sh
source /home/www/MK_dream/bin/activate
killall gunicorn_django
nohup /home/www/MK_dream/bin/gunicorn_django --workers=2 -b 0.0.0.0:9997 --timeout=300&
