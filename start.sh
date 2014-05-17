killall gunicorn_django
NEW_RELIC_CONFIG_FILE=newrelic.ini
export NEW_RELIC_CONFIG_FILE
nohup /home/www/MK_dream/env/bin/newrelic-admin run-program /home/www/MK_dream/env/bin/gunicorn_django --workers=2 -b 127.0.0.1:9997 --timeout=300&
