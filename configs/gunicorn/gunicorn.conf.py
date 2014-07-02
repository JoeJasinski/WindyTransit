bind = "unix:/var/run/django.socket"
logfile = "/var/log/gunicorn.log"
workers = 2
timeout = 120
graceful_timeout = 60