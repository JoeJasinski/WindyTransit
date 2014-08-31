# NEEDS WORK
FROM ubuntu:14.04
MAINTAINER Joe Jasinski

# install the system packages
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools supervisor libpq-dev build-essential
RUN apt-get install -y libgeos-3.4.2 proj-bin gdal-bin libgeos-dev libproj-dev libgdal-dev libproj-dev 
RUN apt-get install -y openssh-server
RUN apt-get install -y nginx

# Install global python packages
RUN easy_install pip 
RUN pip install virtualenv
RUN pip install uwsgi

# create the virtualenv 
RUN virtualenv /site/env/

# install the requirements first so we do not have to install all the time
ADD ./requirements.txt /tmp/requirements.txt

# configure the virtualenv
RUN . /site/env/bin/activate; /site/env/bin/pip install -r /tmp/requirements.txt
ADD . /site/app
RUN mkdir -p /site/var/log/
RUN mkdir -p /site/var/run/
RUN chown -R www-data /site/

# needed for sshd
RUN mkdir /var/run/sshd; chmod 0755 /var/run/sshd

# add the supervisor configs 
ADD ./configs/supervisor/ssh.conf /etc/supervisor/conf.d/ssh.conf
ADD ./configs/supervisor/django.conf /etc/supervisor/conf.d/django.conf
ADD ./configs/supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

# configure nginx
RUN ln -s /site/app/configs/nginx/server.conf /etc/nginx/sites-enabled/server.conf
ADD ./configs/nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

# restart supervisor
RUN service supervisor restart

# collect python static media
RUN /site/env/bin/python /site/app/manage.py collectstatic --noinput

# set django environment variables
ENV DJANGO_ENVIRONMENT_ROOT /site/
ENV DJANGO_LOG_DIR /site/var/log/
ENV DJANGO_DEBUG True

EXPOSE 80 22
CMD ["/usr/bin/supervisord", "-n"]
