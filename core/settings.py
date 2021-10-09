from pathlib import Path
import os
import json
# import dj_database_url

if os.environ.get('HOST', '') == 'HEROKU':
    DEBUG = True if os.environ.get("ENV") in ["DEV", "STAGE"] else False
    HOST = os.environ.get("HOST")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALLOWED_HOSTS = json.loads(os.environ.get("ALLOWED_HOSTS"))
    TIME_ZONE = os.environ.get("TIME_ZONE")
    STORAGE_LINK = os.environ.get("STORAGE_LINK")
    APP_ID = os.environ.get("APP_ID")
    FIREBASE_PROJECT_EMAIL = os.environ.get("FIREBASE_PROJECT_EMAIL")
    FIREBASE_PROJECT_PASS = os.environ.get("FIREBASE_PROJECT_PASS")
    FIREBASE_CONFIG = json.loads(os.environ.get("FIREBASE_CONFIG"))
    if DEBUG:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        EMAIL_HOST_USER = "admin@myproject.com"
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = os.environ.get('EMAIL')
        EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD')
        EMAIL_USE_TLS = True

else:

    try:
        from . import environment
    except ImportError:
        DEBUG = True 
        HOST = 'LOCALHOST'
        SECRET_KEY = "mysecretkey"
        ALLOWED_HOSTS = ['*']
        TIME_ZONE = "UTC"
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        EMAIL_HOST_USER = "admin@myproject.com"
        STORAGE_LINK = "your storage link"
        APP_ID = "your app id"
        IREBASE_PROJECT_EMAIL = "youremail"
        FIREBASE_PROJECT_PASS = "yourpassword"
        FIREBASE_CONFIG = {
            "apiKey": "your api key",
            "authDomain": "your auth domain",
            "projectId": "your project id",
            "databaseURL":"your database url",
            "storageBucket": "your storage bucket",
            "messagingSenderId": "your messaging sender id",
            "appId": "your app id"
        }
    else:
        DEBUG = True if environment.ENV in ["DEV", "STAGE"] else False
        HOST = environment.HOST
        SECRET_KEY = environment.SECRET_KEY
        ALLOWED_HOSTS = environment.ALLOWED_HOSTS
        TIME_ZONE = environment.TIME_ZONE
        STORAGE_LINK = environment.STORAGE_LINK
        APP_ID = environment.APP_ID
        FIREBASE_PROJECT_EMAIL = environment.FIREBASE_PROJECT_EMAIL
        FIREBASE_PROJECT_PASS = environment.FIREBASE_PROJECT_PASS
        FIREBASE_CONFIG = environment.FIREBASE_CONFIG
        if DEBUG:
            EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
            EMAIL_HOST_USER = "admin@myproject.com"
        else:
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_PORT = 587
            EMAIL_HOST_USER = environment.EMAIL
            EMAIL_HOST_PASSWORD = environment.PASSWORD
            EMAIL_USE_TLS = True

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'channels',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
    'posts',
    'games',
    'user_registration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core_files.middleware.CustomAdminPermissionMiddleWare',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

PSQL = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
}

SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DATABASES = {
    'default': PSQL if os.environ.get('HOST', '') == 'HEROKU' else SQLITE
}

# db_from_env = dj_database_url.config()
# DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500

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

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

if not os.environ.get('HOST'):
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

ASGI_APPLICATION = "core.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.core.RedisCache",
        "LOCATION": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        "OPTIONS": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        },
    },
}

AUTH_USER_MODEL = 'user_registration.UserModel'