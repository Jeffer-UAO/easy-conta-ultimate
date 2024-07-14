
import os.path
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))


SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)



ALLOWED_HOSTS = ['*']


# Application definition

SHARED_APPS = [
    'django_tenants',
    'widget_tweaks',
    'django_user_agents',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'core.tenant',
    'core.security',
    'core.user',
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'core.security',
    'core.user',
    'core.login',
    'core.dashboard',
    'core.pos',
    'core.rrhh',
    'core.reports'
]

# INSTALLED_APPS = list(SHARED_APPS) + [
#     app for app in TENANT_APPS if app not in SHARED_APPS
# ]
INSTALLED_APPS = ['django_tenants', 'django.contrib.staticfiles', 'core.tenant', 'widget_tweaks', 'django_user_agents', 'django_cleanup.apps.CleanupConfig', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'core.security', 'core.user', 'core.login', 'core.dashboard', 'core.pos', 'core.rrhh', 'core.reports']



MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.security.context_processors.site_settings',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

def get_db_config(environ_var='DATABASE_URL'):
    """Get Database configuration."""
    options = env.db(var=environ_var, default='sqlite:///db.sqlite3')
    if options['ENGINE'] != 'django.db.backends.sqlite3':
        return options

    # This will allow use a relative to the project root DB path
    # for SQLite like 'sqlite:///db.sqlite3'
    if not options['NAME'] == ':memory:' and not os.path.isabs(options['NAME']):
        options.update({'NAME': os.path.join(BASE_DIR, options['NAME'])})

    return options


db_config = get_db_config()
db_config['ENGINE'] = 'django_tenants.postgresql_backend'

DATABASES = {
    'default': db_config
}



# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django_tenants.postgresql_backend',
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': 'WzivTdJQTorRbgKSgwhqJBqaYyKCDKFA',
#         'HOST': 'viaduct.proxy.rlwy.net',
#         'PORT': '17013',
#     }
# }


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = 'tenant.Scheme'

TENANT_DOMAIN_MODEL = 'tenant.Domain'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'https://41388786.easy-conta-static.pages.dev/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

# Auth

LOGIN_REDIRECT_URL = '/dashboard/'

LOGOUT_REDIRECT_URL = '/login/'

LOGIN_URL = '/login/'

AUTH_USER_MODEL = 'user.User'

# Email

EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Sessions

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SESSION_COOKIE_NAME = 'invoice'

# HTTP

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Constants

GROUPS = {
    'client': 2,
    'employee': 3
}


DOMAIN = env.str('DOMAIN', default='localhost')

DEFAULT_SCHEMA = env.str('DEFAULT_SCHEMA', default='public')