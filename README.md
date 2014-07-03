REQUIREMENTS
-------
1) RECOMMENDED STACK 

 - Ubuntu 14.04
 - Python 2.7
 - Postgresql 9.3 
 - PostGIS 2.x
 - Nginx 1.6
 - Node JS 0.10.26


2) PACKAGE DEPENDENCIES - Ensure the following Apt pacakges are installed:

    build-essential git libfreetype6 libfreetype6-dev libjpeg8-dev libjpeg8 
    libmysqlclient-dev openssh-client openssh-server binutils
    openssl postfix python-virtualenv sqlite3 sudo supervisor zlib1g
    zlib1g-dev libxml2-dev libxslt1-dev python-dev 
    
Needed for mapnik

    libboost-all-dev libmapnik libmapnik-dev mapnik-utils python-mapnik
    
Needed for postgres and postgis

    gdal-bin postgresql-9.3-postgis postgresql-server-dev-9.3 python-psycopg2

Optional but recommended

    ack-grep aptitude curl findutils mlocate graphviz-dev libgraphviz-dev htop
    nmon screen subversion tig tmux vim fail2ban
    
3) GEODJANGO SETUP - Prior to installation, a working GeoDjango Postgres Database is required.

Follow the instructions listed here, ignoreing any environment setup
steps that you already followed. 
http://www.chicagodjango.com/blog/geo-django-quickstart/

4) To get mapnik to work, add this to the PYTHONPATH

    export PYTHONPATH="$PYTHONPATH:/usr/lib/pymodules/python2.7/"

INSTALL
-------

1. Create virtualenv 
    virtualenv  windytransit

2. Activate Virtual Environment
    cd windytransit; . ./bin/activate

3. Make needed directories
    mkdir -p var/log/
    mkdir -p data/
    mkdir proj/; cd proj/

4. Checkout Code
    git clone git@github.com:JoeJasinski/WindyTransit.git windytransit; cd windytransit 

5. Install Python dependencies 
    export PROJECT_DIR=`pwd`
    pip install -r requirements.txt

6. Copy the settings example file into place
    cp mobiletrans/settings/local.example mobiletrans/settings/local.py

7. Adjust the local settings as desired, though the default should be enough to get started

8. Sync the database and migrate the database

   ./manage.py syncdb 
   ./manage.py migrate 


Docker
-------
0) Change directory to the dir with the Dockerfile

1) Build the container
sudo docker build -t windy .

2) Run the container
sudo docker run -itP --rm --name joe windy 

Or, mount the code directory for development

sudo docker run -itP --rm -v `pwd`:/site/app/  --name joe windy
