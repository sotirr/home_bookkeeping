"""
Django settings for home_bookkeeping project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import dynaconf
import django_heroku
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# DB settings for heroku
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600, ssl_require=True
    )
}

# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://dynaconf.readthedocs.io/en/latest/guides/django.html
settings = dynaconf.DjangoDynaconf(
    __name__,
    PRELOAD_FOR_DYNACONF=["../settings.yaml", "../.secrets.yaml"]
)

# Activate Django-Heroku.
django_heroku.settings(settings)

# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
