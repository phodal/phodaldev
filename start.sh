#!/bin/sh
source /home/www/MK_dream/phodal-env/bin/activate
killall gunicorn
NEW_RELIC_CONFIG_FILE=/home/www/MK_dream/MK_dream/newrelic.ini
export NEW_RELIC_CONFIG_FILE
#nohup /home/www/MK_dream/bin/newrelic-admin run-program /home/www/MK_dream/bin/gunicorn --workers=2 MK_dream.wsgi -b 0.0.0.0:9997 --timeout=300& 
nohup /home/www/MK_dream/phodal-env/bin/gunicorn --workers=2 MK_dream.wsgi -b 0.0.0.0:9997 --timeout=300&

