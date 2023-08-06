import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'test'
INSTALL_DIR = '/usr/local/altschool/dynamic-rest/'

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', INSTALL_DIR + 'www/static')

ENABLE_INTEGRATION_TESTS = os.environ.get('ENABLE_INTEGRATION_TESTS', False)

DEBUG = True

DATABASES = {}
if os.environ.get('DATABASE_URL'):
    # remote database
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
else:
    # local sqlite database file
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }

INSTALLED_APPS = (
    'rest_framework',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'xtrm_drest',
    'tests',
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'xtrm_drest.renderers.DynamicBrowsableAPIRenderer'
    )
}

ROOT_URLCONF = 'tests.urls'

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, '../xtrm_drest/static')),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': os.path.abspath(os.path.join(BASE_DIR,
                                '../xtrm_drest/templates')),
        'APP_DIRS': True,
    }
]

xtrm_drest = {
    'ENABLE_LINKS': True,
    'DEBUG': os.environ.get('xtrm_drest_DEBUG', 'false').lower() == 'true'
}
