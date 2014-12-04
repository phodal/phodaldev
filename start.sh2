source /home/www/MK_dream/bin/activate
killall gunicorn_django
NEW_RELIC_CONFIG_FILE=/home/www/MK_dream/MK_dream/newrelic.ini
export NEW_RELIC_CONFIG_FILE
nohup /home/www/MK_dream/bin/newrelic-admin run-program /home/www/MK_dream/bin/gunicorn_django --workers=2 -b 0.0.0.0:9997 --timeout=300&
