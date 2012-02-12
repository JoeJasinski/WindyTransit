ENVIRONMENT SETUP

1. virtualenv --no-site-packages windytransit

2. cd windytransit; . ./bin/activate

3. mkdir proj; cd proj

4. git clone git@github.com:JoeJasinski/WindyTransit.git

5. pip install -r requirements.pip

GEODJANGO SETUP

Follow the instructions listed here, ignoreing any environment setup
steps that you already followed. 
http://www.chicagodjango.com/blog/geo-django-quickstart/


CODE SETUP AND CONFIGURATION

1. Create a settings module as follows and place it on the PYTHON path. 
   NOTE: I have placed this within an VIRTUAL_ENV/etc/django/ directory 
   of which I have included ${VIRTUAL_ENV}/etc/django/ on the PYTHON path.

    mkdir mtsettings
    cd mtsettings
    touch __init__.py
    touch local_settings.py

Edit the local_settings.py file to add the following, making changes where needed: 

    #######################
    #####  These settings should go in local_settings.py
    ####################
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    VENV_ROOT = os.path.join('/','jaz', 'sites', 'mobiletrans')
    PROJECT_ROOT = os.path.join(VENV_ROOT, 'proj', 'mobiletrans')
    
    ADMINS = (
        ('Your Name', 'your_email@example.com'),
    )
    
    MANAGERS = ADMINS
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'mobiletrans',
            'USER': 'mobiletrans_user',
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

