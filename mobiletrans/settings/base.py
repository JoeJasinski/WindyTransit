# Django settings for mobiletrans project.
import os
import environ

default_project_root = environ.Path(__file__) - 2
default_environment_root = default_project_root - 2
default_log_dir = default_environment_root.path('var', 'log')
default_htdocs_dir = default_environment_root.path('htdocs')

default_static_dir = default_project_root.path('static')
default_static_root = default_htdocs_dir.path('static')

default_media_root = default_htdocs_dir.path('media')
default_template_dir = default_project_root.path('templates')


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    
    DJANGO_PROJECT_ROOT=(str, str(default_project_root)),
    DJANGO_ENVIRONMENT_ROOT=(str, str(default_environment_root)),
    DJANGO_LOG_DIR=(str, str(default_log_dir)),
    DJANGO_HTDOCS_DIR=(str, str(default_htdocs_dir)),
    
    DJANGO_STATIC_DIR=(str, str(default_static_dir)),
    DJANGO_STATIC_ROOT=(str, str(default_static_root)),
    
    DJANGO_MEDIA_ROOT=(str, str(default_media_root)),
    DJANGO_TEMPLATE_DIR=(str, str(default_template_dir)),
)
DEBUG = env('DJANGO_DEBUG')
PROJECT_ROOT  = env("DJANGO_PROJECT_ROOT")
ENVIRONMENT_ROOT = env("DJANGO_ENVIRONMENT_ROOT")
LOG_DIR = env("DJANGO_LOG_DIR")
HTDOCS_DIR = env("DJANGO_HTDOCS_DIR")

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': env.db('DJANGO_DATABASE', default='postgis://windytransit@:/windytransit')
#}


GOOGLE_PLACES_API_KEY = ''



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    env("DJANGO_STATIC_DIR"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

COMPRESS_ENABLED=True
COMPRESS_OUTPUT_DIR=''
COMPRESS_CSS_FILTERS=[
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',] 

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9v5=sh2zq5^5-g1x+9q=prax%7jc+xw5%5_+^be!n=z%xk2v=_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    'mobiletrans.mtcore.context_processors.site',
)


ROOT_URLCONF = 'mobiletrans.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    env("DJANGO_TEMPLATE_DIR"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'django_extensions',
    "south", 
    "compressor",
    'rest_framework',
    'djangobower',
    
    'mobiletrans.mtcore',
    'mobiletrans.mtlocation',
    'mobiletrans.mtimport',
    'mobiletrans.mtdistmap',
)


BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'leaflet#0.7.3',
    'leaflet-omnivore#0.3.0',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':os.path.join(LOG_DIR,"mobiletrans.log"),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mobiletrans.mtimport': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

