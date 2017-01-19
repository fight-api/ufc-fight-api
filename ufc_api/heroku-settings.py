from .settings import *
import dj_database_url

DEBUG=False

ALLOWED_HOSTS=["*"]

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES['default'] =  dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
