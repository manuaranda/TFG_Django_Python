"""
Django settings for carpetaPrueba project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
#encoding:utf-8
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))
LOGIN_URL = '/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cx(d4lu^4_0x60(!b29=$#0jq0$xq5b%p$@^l3z2)bk21ci2es'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = (
	'Manuel Aranda Rosales', 'manu.aranda.9@gmail.com',
)


CONSUMER_KEY = 'HSAJYkJso2lx7nV9pHGITg'
CONSUMER_SECRET = 'okILf2DfyyMrNq0JRvlEckNKFC3hFxei21X4NEcURHQ'
ACCESS_KEY = '310810114-eIP0VTRmwJ6uMsBHWb6qzVgp77quUloV3KfGT2MY'
ACCESS_SECRET = 'w2U7z2XcrJHjRDpxMoD0b8lVdSCIMWkZyKckf7oiaHG11'

TEMPLATE_DEBUG = False

APPEND_SLASH=False


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
	'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.admindocs',
	'profile',
	'prueba'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


MEDIA_ROOT = os.path.join(RUTA_PROYECTO,'carga')

ROOT_URLCONF = 'carpetaPrueba.urls'

WSGI_APPLICATION = 'carpetaPrueba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'prueba.db',	
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',		
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(RUTA_PROYECTO,'static'),
)
	
	
SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(RUTA_PROYECTO,'plantillas'),
)
