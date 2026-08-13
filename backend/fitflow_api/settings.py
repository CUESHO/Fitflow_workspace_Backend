from pathlib import Path
import os
from dotenv import load_dotenv
import sys
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
ENV = os.getenv('ENV')
env_path = os.path.join(BASE_DIR, f'.env.{ENV}')
load_dotenv(env_path)
print(f'\nEnvironment: {ENV}')

# Env variables
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL') 
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
TEST_HEADLESS = os.getenv('TEST_HEADLESS') == 'True'
STORAGE_AWS = os.environ.get("STORAGE_AWS") == "True"

# Quick-start development settings - unsuitable for production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
    # Tu app de FitFlow
    "gym_core",
    
    # Jazzmin para el admin
    "jazzmin",

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fitflow_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fitflow_api.wsgi.application"

# Database
# Setup database for testing and production
IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Opciones específicas si en algún momento deciden probar con MySQL
options = {}
if os.environ.get("DB_ENGINE") == "django.db.backends.mysql":
    options = {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'charset': 'utf8mb4',
    }

# --- CÓDIGO LIMPIO: SOLO POSTGRESQL O MYSQL ---
# 1. Si Render inyecta la DATABASE_URL, úsala (Producción)
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600 
        )
    }
# 2. Si no hay URL en la nube, usamos la configuración de tu .env.dev (Local)
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
            'OPTIONS': options,
        }
    }

# Setup de Stripe dependiendo si están en modo test o producción
if IS_TESTING:
    STRIPE_API_USER = os.getenv('STRIPE_API_USER_TEST')
else:
    STRIPE_API_USER = os.getenv('STRIPE_API_USER')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'mi_app/static'),
# ]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Global datetime format
DATE_FORMAT = "d/b/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Email settings
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

#Host settings
HOST = os.getenv('HOST')

#Stripe settings
STRIPE_API_HOST = os.getenv('STRIPE_API_HOST')

# Storage settings
if STORAGE_AWS:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'fitflow_api.storage_backends.StaticStorage'
    
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'fitflow_api.storage_backends.PublicMediaStorage'

    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'fitflow_api.storage_backends.PrivateMediaStorage'
    
    STATIC_ROOT = None
    MEDIA_ROOT = None
else:
    # Local development 
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

# Cors
CORS_ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')

# ==========================================
# JAZZMIN SETTINGS (FITFLOW ADMIN)
# ==========================================
JAZZMIN_SETTINGS = {
    "site_title": "FitFlow Admin",
    "site_header": "FitFlow",
    "site_brand": "FitFlow Dashboard",
    "welcome_sign": "Bienvenido al control de afluencia de FitFlow",
    "copyright": "Aarón Castañeda © 2026",
    "search_model": ["gym_core.Miembro"],
    
    # Menú superior
    "topmenu_links": [
        {"name": "Inicio",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Frontend Angular", "url": "http://localhost:4200", "new_window": True},
    ],

    # Íconos para tus 5 tablas
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "gym_core.Area": "fas fa-map-marker-alt",
        "gym_core.Miembro": "fas fa-dumbbell",
        "gym_core.RegistroAcceso": "fas fa-clock",
        "gym_core.Suscripcion": "fas fa-id-card",
        "gym_core.TipoMembresia": "fas fa-tags",
    },
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False, 
}

# Forzar el modo oscuro
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "dark_mode_theme": "darkly",
}