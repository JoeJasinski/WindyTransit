bind = "unix:/site/var/run/django.socket"
logfile = "/site/var/log/gunicorn.log"
workers = 2
timeout = 120
graceful_timeout = 60