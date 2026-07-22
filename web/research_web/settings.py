from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = "django-insecure-change-this-for-production"


DEBUG = True


ALLOWED_HOSTS = []


INSTALLED_APPS = [

    "django.contrib.staticfiles",

    "dashboard",

]


MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.middleware.common.CommonMiddleware",

]


ROOT_URLCONF = "research_web.urls"


TEMPLATES = [

    {

        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [

            BASE_DIR
            / "web"
            / "dashboard"
            / "templates"

        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [],

        },

    },

]


WSGI_APPLICATION = "research_web.wsgi.application"


DATABASES = {

    "default": {

        "ENGINE": "django.db.backends.sqlite3",

        "NAME": BASE_DIR / "research.db",

    }

}


LANGUAGE_CODE = "en-us"


TIME_ZONE = "UTC"


USE_I18N = True


USE_TZ = True


STATIC_URL = "static/"


STATICFILES_DIRS = [

    BASE_DIR
    / "web"
    / "dashboard"
    / "static"

]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
