"""
Django settings for gpsstops project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wp_jd0y3d+9_=(+ccf(gqz3uigk)sar6(mwclm@xr5*9#)o6#_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True

SITE_ID = 1
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',

    'swampdragon',
    'swampdragon_auth',
    'swampdragon_notifications',

    'push_notifications',

    'django_cron',

    # 'django_wysiwyg',
    'ckeditor',

    'maps',
    'appointments',
    'custom_forms',
    'products',
    'services',

    'siteadmin',

    # 'corsheaders',
)

LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in

MIDDLEWARE_CLASSES = (
    # 'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gpsstops.urls'

WSGI_APPLICATION = 'gpsstops.wsgi.application'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# For PythonAnwhere Server
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'gpsstops$gps_new_db',
#         'USER': 'gpsstops',
#         'PASSWORD': 'root',
#         'HOST': 'mysql.server',
#         'PORT': '3306',
#     }
# }

# For new server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bennyapp_django',
        'USER': 'bennyapp',
        'PASSWORD': '2~Pdo4c1',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'bennyapp.sqlite3',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# For Local Server
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'gps_new_db',
#        'USER': 'root',
#        'PASSWORD': 'root',
#        'HOST': 'localhost',
#        'PORT': '3306',
#
#    }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )


REST_FRAMEWORK = {

    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',


    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    )
}

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bennyappservice@gmail.com'
EMAIL_HOST_PASSWORD = 'benny@1234'
EMAIL_PORT = 587



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

PUSH_NOTIFICATIONS_SETTINGS = {
    "GCM_API_KEY": "AIzaSyBTA_HmUCfTNxR_ugDTtubDJ8DG6rgspI0"
}

GCM_API_KEY = "AIzaSyBTA_HmUCfTNxR_ugDTtubDJ8DG6rgspI0"
CERT_FILE = BASE_DIR + '/certs/gpsstops_cer.pem'
KEY_FILE = BASE_DIR + '/certs/agpsstops_key1.pem'
DEV_CERT_FILE = BASE_DIR + '/certs/gpsstops-dev.pem'


# SwampDragon settings
SWAMP_DRAGON_CONNECTION = ('swampdragon_notifications.notification_connection.Connection', '/data')
DRAGON_URL = 'http://localhost:9999/'
SWAMP_DRAGON = {
    'foo': 'bar'
}


SWAMP_DRAGON_NOTIFICATION_BACKENDS = [
    ('realtime', 'swampdragon_notifications.backends.realtime_notifications.RealtimeNotification'),
    # ('email', 'swampdragon_notifications.backends.email_notifications.EmailNotification'),
]


SWAMP_DRAGON_NOTIFICATIONS = {
    'foo': {
        'processor': 'appointments.subject_renderer.get_appointments',
        'icon': 'http://placekitten.com/g/64/64'
    }
}

SWAMP_DRAGON_HEARTBEAT_ENABLED = True
SWAMP_DRAGON_HEARTBEAT_FREQUENCY = 1000 * 30  # Five minutes

CRON_CLASSES = [
    "appointments.cron.NotificationsCronJob",
]

SERVER_URL = 'http://bennyapp.com'

# DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}

try:
    from local_settings import *
except:
    pass
