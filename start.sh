killall gunicorn_django
NEW_RELIC_CONFIG_FILE=newrelic.ini
export NEW_RELIC_CONFIG_FILE
nohup /root/Blog/bin/newrelic-admin /root/Blog/bin/gunicorn_django --workers=2 -b 0.0.0.0:9997 --timeout=300&
