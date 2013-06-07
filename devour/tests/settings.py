SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'devour-tests.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'devour',
    'devour.tests',
)

ROOT_URLCONF = 'devour.tests.urls'

SECRET_KEY = 'any-key'
