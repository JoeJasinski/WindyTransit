FROM ubuntu:14.04
MAINTAINER Joe Jasinski
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools supervisor libpq-dev build-essential
RUN apt-get install -y libgeos-3.4.2 proj-bin gdal-bin libgeos-dev libproj-dev libgdal-dev libproj-dev 
RUN apt-get install -y openssh-server
RUN apt-get install -y nginx
RUN easy_install pip 
RUN pip install virtualenv
RUN pip install uwsgi
RUN virtualenv /site/env/
ADD ./requirements.txt /tmp/requirements.txt
RUN . /site/env/bin/activate; /site/env/bin/pip install -r /tmp/requirements.txt
ADD . /site/app
RUN mkdir -p /site/var/log/
RUN mkdir -p /site/var/run/
RUN chown -R www-data /site/

RUN mkdir /var/run/sshd; chmod 0755 /var/run/sshd

ADD ./configs/supervisor/ssh.conf /etc/supervisor/conf.d/ssh.conf
ADD ./configs/supervisor/django.conf /etc/supervisor/conf.d/django.conf
ADD ./configs/supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

RUN ln -s /site/app/configs/nginx/server.conf /etc/nginx/sites-enabled/server.conf

ADD ./configs/nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN service supervisor restart
RUN /site/env/bin/python /site/app/manage.py collectstatic --noinput

ENV DJANGO_ENVIRONMENT_ROOT /site/
ENV DJANGO_LOG_DIR /site/var/log/
ENV DJANGO_DEBUG True

EXPOSE 80 22
CMD ["/usr/bin/supervisord", "-n"]
