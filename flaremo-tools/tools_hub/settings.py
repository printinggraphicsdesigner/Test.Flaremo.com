import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-flaremo-tools-2026-change-this-in-production!'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'translator',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'tinymce',
    'pages',
    'blog',
    'accounts',
    'subscriptions',    

    'core',
    'word_to_pdf',
    'image_to_video',
    'image_to_text',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tools_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.dynamic_blogs',
            ],
        },
    },
]

WSGI_APPLICATION = 'tools_hub.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ================= MEDIA FILES =================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'







TINYMCE_DEFAULT_CONFIG = {
    'height': 600,
    'width': '100%',
    'menubar': 'file edit view insert format tools table help',
    'plugins': '''
        advlist autolink lists link image charmap print preview anchor 
        searchreplace visualblocks code fullscreen insertdatetime media 
        table paste code help wordcount
    ''',
    'toolbar': '''
        undo redo | formatselect | bold italic backcolor | 
        alignleft aligncenter alignright alignjustify | 
        bullist numlist outdent indent | removeformat | image | link | table | code
    ''',
    'image_advtab': True,
    'paste_data_images': True,
}