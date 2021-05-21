from .base import *
import cloudinary
import cloudinary_storage

DEBUG = False

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage'
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "fashioncartbd",
    'API_KEY': os.environ.get("cloudinary_api_key"),
    'API_SECRET': os.environ.get("cloudinary_api_secret"),
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "midllewares.cart.CartMiddleware"
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'production_db.sqlite3',
    }
}


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

