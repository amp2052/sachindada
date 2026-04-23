from pathlib import Path
import os
from decouple import config
import dj_database_url

# ===========================
# BASE DIRECTORY
# ===========================

BASE_DIR = Path(__file__).resolve().parent.parent


# ===========================
# SECURITY
# ===========================

SECRET_KEY = config("SECRET_KEY", default="django-insecure-temp-key-change-this")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('mr', 'Marathi'),
]

USE_I18N = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # MUST be after SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]
# ===========================
# APPLICATION DEFINITION
# ===========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
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

ROOT_URLCONF = "projectt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "projectt.wsgi.application"


# ===========================
# DATABASE
# ===========================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,
    )
}


# ===========================
# PASSWORD VALIDATION
# ===========================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ===========================
# INTERNATIONALIZATION
# ===========================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# ===========================
# STATIC & MEDIA FILES ✅✅✅
# ===========================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ===========================
# DEFAULT PRIMARY KEY
# ===========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===========================
# EMAIL CONFIG ✅ (SECURE)
# ===========================

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
# EMAIL_HOST_PASSWORD = "pzhw mbrj qcux suyq"

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "amp2052@gmail.com"
EMAIL_HOST_PASSWORD = "pzhw mbrj qcux suyq"  # Use App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# ===========================
# EXTERNAL API KEYS (SAFE)
# ===========================
