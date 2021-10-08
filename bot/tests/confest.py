import os

import pytest
from django.conf import settings
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', 5432),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
    }
