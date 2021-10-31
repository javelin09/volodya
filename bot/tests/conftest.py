import os

import pytest
from django.conf import settings
from dotenv import load_dotenv

from users.models import TelegramUser


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


@pytest.fixture
def get_telegram_admin_user_id():
    return TelegramUser.objects.filter(is_admin=True).first().telegram_id


@pytest.fixture
def get_telegram_user_id():
    return TelegramUser.objects.filter(is_admin=False).first().telegram_id
