import os
import sys
from pathlib import Path

import dj_database_url
import sqids
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "True") == "True"

if os.environ.get("SECRET_KEY"):
    SECRET_KEY = os.environ["SECRET_KEY"]
elif DEBUG:
    SECRET_KEY = get_random_secret_key()
    is_testing: bool = len(sys.argv) > 1 and sys.argv[1] == "test"
    if not is_testing:
        print(
            "WARNING: No SECRET_KEY set — generated a development key. "
            "Add SECRET_KEY=<the key below> to your base.env to persist.",
            file=sys.stderr,
        )
        print(SECRET_KEY, file=sys.stderr)
else:
    raise RuntimeError("SECRET_KEY must be set in production")

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shortr",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "ui/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
DATABASES = {"default": dj_database_url.config(default="sqlite:///db.sqlite3")}


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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "ui/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Other
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SQID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SQID_MIN_LEN = 6

DEFAULT_SQID = sqids.Sqids(
    alphabet=SQID_ALPHABET,
    min_length=SQID_MIN_LEN,
)
