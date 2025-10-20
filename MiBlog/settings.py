"""
Django settings for MiBlog project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# === Paths & env ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # en Render no hay .env: usa Environment Variables

# Helpers para castear desde env
def _env_bool(name: str, default: str = "False") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default

# === Core ===================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = _env_bool("DEBUG", "True")

# En prod, define esto en Render: ALLOWED_HOSTS=miblog2.onrender.com,tu-dominio.cl
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()
]

# CSRF Trusted Origins (útil para Render/domino propio)
# En Render, pon: CSRF_TRUSTED_ORIGINS=https://miblog2.onrender.com,https://tu-dominio.cl,https://www.tu-dominio.cl
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# === Apps ===================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "miapp",  # tu app
]

# === Middleware =============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <- sirve estáticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MiBlog.urls"

# === Templates ==============================================================
TEMPLATES_DIR = BASE_DIR / "templates"  # si no existe, no pasa nada
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "MiBlog.wsgi.application"

# === Database ===============================================================
# Blog simple: SQLite (Render lo soporta para cosas pequeñas)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# === Password validation ====================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === I18N / TZ ==============================================================
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# === Static files (WhiteNoise) ==============================================
# En build (Render) ejecuta: python manage.py collectstatic --noinput
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # aquí collectstatic copia todo

# Si tienes carpeta "static" a nivel de proyecto, la agregamos condicionalmente.
if (BASE_DIR / "static").exists():
    STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise: archivos comprimidos y con hash
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# === Email (desde env) ======================================================
# Para desarrollo puedes usar: EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend").strip()
EMAIL_HOST = os.getenv("EMAIL_HOST", "").strip()
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").strip().lower() in ("1","true","yes","on")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").strip().lower() in ("1","true","yes","on")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "15"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip()
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "").strip()
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "webmaster@localhost").strip()

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]


# Destinatarios para tu formulario (coma-separado en env)
CONTACT_RECIPIENTS = [
    e.strip() for e in os.getenv("CONTACT_RECIPIENTS", "").split(",") if e.strip()
]

# === Security en producción =================================================
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", "True")
    SECURE_HSTS_SECONDS = _env_int("SECURE_HSTS_SECONDS", 3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True")
    SECURE_HSTS_PRELOAD = _env_bool("SECURE_HSTS_PRELOAD", "True")
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# === Logging mínimo (útil en Render) =======================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# === Default PK =============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

