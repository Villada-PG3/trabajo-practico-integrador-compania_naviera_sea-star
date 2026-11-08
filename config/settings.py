
"""
Django settings for config project.
"""

from pathlib import Path

# DIRECTORIO PRINCIPAL

BASE_DIR = Path(__file__).resolve().parent.parent


# SEGURIDAD

SECRET_KEY = 'django-insecure-m@hzef5aa07e*)0ib#zwqjv1v7m$55%kb1@_%j#&vo$8207i@9'

DEBUG = True

ALLOWED_HOSTS = []


# APLICACIONES INSTALADAS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compania_naviera',
]


# MIDDLEWARE

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# CONFIGURACIÓN GENERAL

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# PLANTILLAS

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

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


# BASE DE DATOS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# VALIDACIÓN DE CONTRASEÑAS

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


# IDIOMA Y HORARIO

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_TZ = True


# ARCHIVOS ESTÁTICOS

STATIC_URL = 'static/'


# CONFIGURACIÓN DE EMAIL

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# AUTENTICACIÓN

LOGIN_REDIRECT_URL = 'home'

LOGIN_URL = 'login'


# CLAVE PRIMARIA POR DEFECTO

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
