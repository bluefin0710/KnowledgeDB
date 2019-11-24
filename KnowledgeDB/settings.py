"""
Django settings for KnowledgeDB project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'crw@l2-6pgk-dfhwi!e8g2b(!9)db38jtl=70f_0g-6lo0^gmb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

#STATC_ROOT = os.path.join(BASE_DIR,'static')
ALLOWED_HOSTS = ['localhost','127.0.0.1','.pythonanywhere.com']
#ALLOWED_HOSTS = ['.pythonanywhere.com']
#ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts.apps.PostsConfig',   #App
    'bootstrap4',  # django-bootstrap4
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'KnowledgeDB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dbsite.context_processors.common',
            ],
            'builtins':[
                'bootstrap4.templatetags.bootstrap4', # ここに追加！
            ],
        },
    },
]

WSGI_APPLICATION = 'KnowledgeDB.wsgi.application'
#WSGI_APPLICATION = 'nmcmh01.pythonanywhere.com.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# MySQL Setting
# import pymysql
# pymsql.install_as_MySQLdb()
#

DATABASES = {
        'default': {
                'ENGINE':'django.db.backends.mysql',
#                 'NAME':'masterdb',
#                 'USER':'root',
#                 'HOST':'127.0.0.1',
                 'NAME':'nmcmh01$MasterDB',
                 'USER':'nmcmh01',
                 'HOST':'nmcmh01.mysql.pythonanywhere-services.com',
                 'PASSWORD':'mysqlroot',
                 'PORT':'3306',
                 'AUTOMIC_REQUESTS':True,
##                 'OPTIONS': {
##                         'read_default_file': '/path/to/my.cnf',
#                          'charset': 'utf8mb4',
#                          'sql_mode': 'TRADITONAL,NO_AUTO_VALUE_ON_ZERO',
### my.cnf
##[client]
##database = NAME
##user = USER
##password = PASSWORD
##default-character-set = utf8
#
##                         }
        }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

LOGIN_URL = 'posts:login'
LOGIN_REDIRECT_URL = 'posts:index_listview'

#LOGIN_REDIRECT_URL = '../../posts/'
LOGOUT_REDIRECT_URL = '../../'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#MEDIA_URL = '/pics/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'),
#]
