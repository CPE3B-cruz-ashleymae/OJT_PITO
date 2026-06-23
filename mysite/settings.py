import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=3cwe#0n-@!k2l8qouqfvgq*w^4*o0u4u4iluc_i-ys2hscf0@'
DEBUG = True

ALLOWED_HOSTS = ['210.5.122.11', '210.5.122.11.nip.io', '172.26.91.55', '172.26.91.55.nip.io', 'localhost', '127.0.0.1']

# --- PROXY AND SECURITY SETTINGS ---
CSRF_TRUSTED_ORIGINS = ['http://172.26.91.55.nip.io', 'https://172.26.91.55.nip.io']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # ✅ Fixed: was 'http'
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
# -----------------------------------

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_UNIQUE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'blog' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'blog/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SITE_ID = 1
ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ashleymaecruz126@gmail.com'
EMAIL_HOST_PASSWORD = 'ihskjfdmhytyqtgx'

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

LOGIN_URL = 'login'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'  # ✅ Fixed: was 'http'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

# --- LOGIN / LOGOUT REDIRECTS ---
LOGIN_REDIRECT_URL = 'blog-home'      # Redirects to your blog home after login
LOGOUT_REDIRECT_URL = 'blog-home'     # Redirects to your blog home after logout

# Allauth specific redirects
ACCOUNT_LOGIN_REDIRECT_URL = 'blog-home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'blog-home'
SOCIALACCOUNT_LOGIN_ON_GET = True     # Skips the "confirm" screen on Google login
