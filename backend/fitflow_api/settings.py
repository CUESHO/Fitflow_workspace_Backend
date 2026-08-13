"""
Configuración de Django para el proyecto FitFlow.

Backend: Django REST Framework
Base de datos: PostgreSQL (FitFlow_Workspace)
Panel de administración: Jazzmin
"""

import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# .env define únicamente ENV (dev | prod); luego se carga .env.<ENV>
#
# override=False es importante: en Render las variables reales (DATABASE_URL,
# SECRET_KEY...) ya viven en el entorno y NO deben ser pisadas por el archivo
# .env.prod del repositorio, que sólo contiene valores de ejemplo.
load_dotenv(BASE_DIR / ".env", override=False)
ENV = os.getenv("ENV", "dev")
load_dotenv(BASE_DIR / f".env.{ENV}", override=False)
print(f"\nEnvironment: {ENV}")


def csv_env(nombre, default=""):
    """Convierte 'a,b,c' en ['a', 'b', 'c'] descartando valores vacíos.

    Sin esto, ''.split(',') devuelve [''] y Django/CORS fallan.
    """
    return [valor.strip() for valor in os.getenv(nombre, default).split(",") if valor.strip()]


SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-solo-para-desarrollo")
DEBUG = os.getenv("DEBUG", "False") == "True"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

ALLOWED_HOSTS = csv_env("ALLOWED_HOSTS", "127.0.0.1,localhost")

# Render publica el dominio de la app en esta variable de entorno.
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ==========================================
# APLICACIONES
# ==========================================
INSTALLED_APPS = [
    # Jazzmin debe ir ANTES de django.contrib.admin para reemplazar sus plantillas.
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # whitenoise.runserver_nostatic va antes de staticfiles.
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Librerías de terceros
    "rest_framework",
    "django_filters",
    "corsheaders",
    # Aplicación propia de FitFlow
    "gym_core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # CorsMiddleware debe ir lo más arriba posible y antes de CommonMiddleware.
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fitflow_api.urls"
WSGI_APPLICATION = "fitflow_api.wsgi.application"

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

# ==========================================
# BASE DE DATOS (PostgreSQL, nunca sqlite3)
# ==========================================
IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

if os.getenv("DATABASE_URL"):
    # Producción: Render inyecta DATABASE_URL automáticamente.
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    # Desarrollo local: datos tomados de .env.dev
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# ==========================================
# DJANGO REST FRAMEWORK
# ==========================================
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Sin paginación: la API devuelve una lista simple, que es lo que
    # consumen los servicios de Angular con get<T[]>().
    "DEFAULT_PAGINATION_CLASS": None,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ==========================================
# CORS (para que Angular pueda consumir la API)
# ==========================================
CORS_ALLOWED_ORIGINS = csv_env("ALLOWED_ORIGINS", "http://localhost:4200")
CSRF_TRUSTED_ORIGINS = [
    origen for origen in CORS_ALLOWED_ORIGINS if origen.startswith("http")
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# ==========================================
# VALIDACIÓN DE CONTRASEÑAS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==========================================
# INTERNACIONALIZACIÓN
# ==========================================
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

DATE_FORMAT = "d/b/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================
# ARCHIVOS ESTÁTICOS (servidos por WhiteNoise)
# ==========================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Comprime los estáticos sin generar manifiesto. Se evita
        # CompressedManifestStaticFilesStorage porque Jazzmin referencia
        # archivos que no siempre existen y rompería el collectstatic.
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ==========================================
# SEGURIDAD EN PRODUCCIÓN
# ==========================================
if not DEBUG:
    # Render entrega el tráfico por HTTPS a través de su proxy.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ==========================================
# JAZZMIN (PANEL DE ADMINISTRACIÓN)
# ==========================================
JAZZMIN_SETTINGS = {
    "site_title": "FitFlow Admin",
    "site_header": "FitFlow",
    "site_brand": "FitFlow Dashboard",
    "welcome_sign": "Bienvenido al control de afluencia de FitFlow",
    "copyright": "Aarón Castañeda",
    "search_model": ["gym_core.Miembro"],
    "topmenu_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API REST", "url": "/api/", "new_window": True},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "gym_core.Miembro": "fas fa-dumbbell",
        "gym_core.TipoMembresia": "fas fa-tags",
        "gym_core.Area": "fas fa-map-marker-alt",
        "gym_core.Suscripcion": "fas fa-id-card",
        "gym_core.RegistroAcceso": "fas fa-clock",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "dark_mode_theme": "darkly",
}
