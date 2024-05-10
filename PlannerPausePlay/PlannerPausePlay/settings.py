from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR =Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%ri+qjt7ybk=54euusv8l@t$%nw&37tl&%9^zt0nbbud72uv7a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'VacayVue',
    'members',
]
AUTH_USER_MODEL = 'VacayVue.CustomUser'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'VacayVue.backends.EmailBackend'
]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # Replace 'smtp.example.com' with your SMTP server address
EMAIL_PORT = 587  # Replace 587 with your SMTP port number
EMAIL_USE_TLS = True  # Set it to True if TLS is required, otherwise set it to False
EMAIL_HOST_USER = 'your_email@example.com'  # Replace with your email address used for authentication
EMAIL_HOST_PASSWORD = 'your_email_password'  # Replace with your email password
DEFAULT_FROM_EMAIL = 'your_email@example.com'  # Replace with your default sender email address



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


ROOT_URLCONF = 'PlannerPausePlay.urls'

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
                'VacayVue.context_processors.current_year',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'PlannerPausePlay.wsgi.application'


# Database


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vacayvue',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',  # Set to the address of your MySQL server
        'PORT': '3306',       # Set to the port of your MySQL server
          'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/' #with or without slash at beginning	
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'members', 'static'),
    os.path.join(BASE_DIR, 'VacayVue', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


