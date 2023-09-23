"""
Django settings for BaazaarAPI project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i-m5upsay3#&bwh+gdi(6$1r5kl#vv$_vjo76#387t^9t!clw*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID=1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # 'drf_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'rest_framework',


    ##apps
    'user',
    'products',
    'orders',
    'payment',



    ##config
    'phonenumber_field',
    'django_countries',
    'randompinfield',
    'rest_auth',
    'allauth', 
    'allauth.account',
    'allauth.socialaccount', 
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.twitter.client',
    'rest_framework.authtoken', 
    'social_django',
    'corsheaders',
    'rest_social_auth',
    #'drf_social_oauth2',
    'oauth2_provider',
    #'social_auth',
    'django_filters',

    # Django Elasticsearch integration
    'django_elasticsearch_dsl',
    # Django REST framework Elasticsearch integration (this package)
    'django_elasticsearch_dsl_drf',
    'haystack',




    


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AuthenticationMiddleware',
    # 'allauth.socialaccount.middleware.SocialAccountMiddleware', 
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

]



ROOT_URLCONF = 'BaazaarAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect', # <-- Her
            ],
        },
    },
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '47b8cd5c1b4d217f740c',
            'secret': '8edb48020b6200230ede857b5e1affa494387a12',
            'key': ''
        }
    }, 
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '608206504022-8udhlptn91o7tmq25clg7klmkloe7dus.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',  # Replace with your Elasticsearch server details
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://localhost:9200/',  # Replace with your Elasticsearch server URL
        'INDEX_NAME': 'my_index',  # Replace with your desired index name
    },
}


REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  
    #    'drf_social_oauth2.authentication.SocialAuthentication',
   )
}
CORS_ALLOWED_ORIGINS = [
   "http://localhost:8000",
   "http://127.0.0.1:8000"
]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#TWILIO SETTINGS
TWILIO_ACCOUNT_SID=config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= config('TWILIO_TOKEN')
TWILIO_FROM_NUMBER=config('TWILIO_FROM')

#EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Use your own broker URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Use your own result backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

#TWITTER CONFIG
SOCIAL_AUTH_TWITTER_KEY = 'wTLpUQeuPo9V3I7hvHuZECLcY' 
SOCIAL_AUTH_TWITTER_SECRET = 'o7yyzXXExsVRjNnBp1Jk5Bihp4IZNTgQHiwePqLAioNGE8CkIX'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

#GOOGLE CONFIG
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '608206504022-8udhlptn91o7tmq25clg7klmkloe7dus.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
# LOGIN_URL = 'login'  # Set this to your login view name.
# LOGIN_REDIRECT_URL = 'profile/1/'  # Set this to your desired post-login redirect URL.




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
