import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

SECRET_KEY = '༼ つ ◕_◕ ༽つ'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'precept',
        'USER': 'precept',
        'PASSWORD': 'precept',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'drf_auth_service'
]

AUTH_USER_MODEL = 'drf_auth_service.SSOUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'apps.common.middlewares.ApiMiddleware',
]

ROOT_URLCONF = 'urls'

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
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%SZ",
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': ['drf_auth_service.common.backends.SSOAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}


FIXTURE_DIRS = (
    'fixtures/',
)

# SSO = {
#     "SERIALIZERS": {
#         "REGISTER_SERIALIZER": "apps.authentication.serializers.RegisterSerializer",
#         "SEND_RESET_PASSWORD_SERIALIZER": "apps.authentication.serializers.ResetPasswordSerializer"
#     },
#     "VIEWS": {
#         "USER_VIEWS": "apps.users.views.CustomUserViewSet",
#     },
#     "BACKENDS": {
#         "SMS_BACKEND": "apps.common.backends.CustomPhoneProvider",
#         "REGISTER_BACKENDS": [
#             'apps.common.backends.CustomRegisterBackend',
#         ]
#     }
# }
