from pathlib import Path
import os
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

#CORS_ALLOW_CREDENTIALS = True
#ALLOWED_HOSTS = ['*']
# CORS: orígenes permitidos
# Alternativa (más segura que permitir todos los orígenes)
# CORS_ALLOW_ALL_ORIGINS = False  # Recomendado
#CORS_ALLOW_ALL_ORIGINS = True  # Solo para pruebas locales rápidas

"""
CORS_ALLOWED_ORIGINS = [
    "https://icarpiocvonline.onrender.com",
    "https://lanoria.onrender.com",
    "https://albertaapi.onrender.com",
    "http://localhost:3000"
]   
"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken', 
    'minigames',
    'stories',
    'cluedo',
    'tarotapi',
    'invoices',
    'cvonline',
    'traductor',
    'interpreter',
    'horoscope',
    'napolipizza',
    'assistants'
     
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'minigames.utils.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 resultados por página
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'albertaapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'albertaapi.wsgi.application'

# Muy importante: Exponer los headers que quieres leer
CORS_EXPOSE_HEADERS = ['Content-Disposition']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),      
        'USER': os.getenv('DB_USER'),      
        'PASSWORD': os.getenv('DB_PASSWORD'), 
        'HOST': os.getenv('DB_HOST'),      
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'options': '-c search_path=albertaapif',  # Esquema diferente por cada app
        },
    }
}

AUTH_USER_MODEL = 'minigames.User'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'  # Siempre debe empezar y terminar con / para producción

if DEBUG:
    # En desarrollo
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    # En producción
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Send Mails

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD =  os.getenv('EMAIL_PWD')
