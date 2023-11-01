import os
import json
from pathlib import Path
from dotenv import load_dotenv

# load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '5y&i0l)iuy-$v!7e7fdfbz6mfga#jqt2gbg+$kpj9w=l#uvo1q'
SECRET_KEY = 'django-insecure-#aegk2y33xdxk5unok)q_ivkkbj!kiy=momow00x@z+lo7b5$f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']#['192.168.150.54']

# Application definition
CUSTOM_APPS =[
"user",
'brokers',

]

# MIGRATION_MODULES = {
#     **{'auth': None,
#     'admin':None,
#     'contenttypes': None,
#     'sessions': None,},
#     **{x:None for x in CUSTOM_APPS}
# }


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'rest_framework_simplejwt',
    'celery',
]+CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'custom_lib.custom_middleware.ErrorHandlerMiddleware',
]

ROOT_URLCONF = 'WINR.urls'

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

WSGI_APPLICATION = 'WINR.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
envs = os.environ
# HOST_SERVER = envs.get("HOST_SERVER","http://localhost:8000")
# DB_NAME = envs.get("DB_NAME","")
# DB_USER = envs.get("DB_USER","")
# DB_PASSWORD = envs.get("DB_PASSWORD","")
# DB_SERVER = envs.get("DB_SERVER","")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': DB_NAME,
#         'USER':DB_USER,
#         'PASSWORD':DB_PASSWORD,
#         'HOST':DB_SERVER,
#         'PORT':3306,
#         'CONN_MAX_AGE':None

#     }
# }

# DATABASES = {
#      "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "admin",
#         "USER": "admin",
#         "PASSWORD": "password",
#         "HOST": "database",
#         "PORT": 5432,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'custom_lib.authentication.ClientAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': ['custom_lib.renderer.JSONResponseRenderer'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "JWT authorization"
        }, 'basic': {
            'type': 'basic'
        }
    },
    'JSON_EDITOR': True,
    'TAGS_SORTER':'alpha',
    # 'FILTER':'tags'
    'MAX_DISPLAYED_TAGS':1
}

ERROR_FILE_PATH=os.path.join(BASE_DIR,"error_code.json")
ERROR_JSON={}
try:
    ERROR_JSON = json.loads(open(ERROR_FILE_PATH).read())
except Exception as e:
    print(e)

CORS_ORIGIN_ALLOW_ALL = True
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + ['userId','token','jwtToken','newToken']

JWT_EXPIRATION_IN_MINUTES = 60

# env vars
LOG_DELETION=envs.get('LOG_DELETION_DAY', 15)
# JWT_EXPIRATION_IN_MINUTES=envs.get("JWT_EXPIRATION_IN_MINUTES")

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
