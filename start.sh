killall gunicorn_django
nohup gunicorn_django --workers=2 -b 127.0.0.1:9997&
