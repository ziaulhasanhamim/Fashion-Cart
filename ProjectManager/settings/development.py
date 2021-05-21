from .base import *

DEBUG = True
SECRET_KEY = 'ijng1yfdsfsdfsdfsdfln(gqx15qpjusofga-ww82ds4$jdmnh7uo4&5w&fva7!'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'NAME': BASE_DIR / 'development_db.sqlite3',
    }
}
