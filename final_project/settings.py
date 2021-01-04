"""
Django settings for final_project project.

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
SECRET_KEY = '$54m8ykngs@1#8v!j!^l#w24m9y&tsy=g55l!vk6(yzo)!e6_%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_FROM_EMAIL = "<ellyzyaory@gmail.com>"
try:
    from .email_settings import host,user, password
    EMAIL_HOST = host #"smtp.gmail.com"
    EMAIL_HOST_USER = user #"ellyzyaory@gmail.com"
    EMAIL_HOST_PASSWORD = password #"password"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
except:
    pass

SITE_URL = "http://eightery.com"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'final',
    'django_extensions',

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


ROOT_URLCONF = 'final_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [r'C:\Users\Johanes\project\final_project\final\templates'],
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

WSGI_APPLICATION = 'final_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_TAX_RATE = 0.08

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"final_project", "static", "static_root")
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR),"final_project", "static", "static_files", "img"),
    os.path.join(os.path.dirname(BASE_DIR), "final_project", "final", "static", "img"),
    #r'C:\Users\Johanes\project\final_project\static\static\static_files',
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "final_project", "static", "media")

STRIPE_SECRET_KEY = "sk_test_51HtT5gBc2FlQjGOxTQDldaTNQlYWsX9xkWv7WORTjzFKYGqnqQ3DThem2xKozHLQHLBvszOt5hiDKH4QpFpjqKJC004yMuDJ0P"
STRIPE_PUBLISHABLE_KEY = "pk_test_51HtT5gBc2FlQjGOxXZcCWUnl4vIFOiSYG47SngEm7YjFvg23PTfifkkqpITBNOXUMJYF3h9Fo7iv6f6soFOdu89g00koLKnksg"
