import datetime
import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = strtobool(os.getenv('DEBUG'))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bot',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', 5432),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOT_TOKEN = os.getenv('BOT_TOKEN')

TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'

CURRENT_YEAR = datetime.datetime.now().year

WELCOME_TEXT = 'Здарова, демон.' \
               '\nИспользуй команду /voice, если хочешь услышать мой бархатный голосок.' \
               '\nКоманду /flip_coin, если хочешь, чтобы монетка решила за тебя, тряпка.' \
               '\nКоманду /balaboba фраза, если хочешь, чтобы я тебе пацанскую цитату подогнал.' \
               f'\nКоманду /remind Купить аспирин - 01.01.{CURRENT_YEAR} 12:00, ' \
               f'если хочешь, чтобы я тебе напомнил о чем-то.' \
               '\nКоманду /weather город, если хочешь узнать прогноз погоды в конкретном городе.' \
               '\nДобавь меня в групповой чат, если хочешь, чтобы я отвечал на ругательные ' \
               'сообщения пользователей.' \
               '\nКоманду /add_swear слово, чтобы добавить новое ругательство в базу данных. ' \
               'Доступно только администратору бота.' \
               '\nКоманду /holiday_greeting Текст поздравления - 12.01.2022 14:00 - all/<user_id>, ' \
               'чтобы Володя отправил текст поздравления конкретному пользователю, либо всем сразу. ' \
               'Доступно только администратору бота.' \
               '\n\nАвтор сия творения - @sh4rpy.'

BALABOBA_COMMAND_ERROR_TEXT = 'Ты конченный? После команды напиши фразу, которую дополнит Балабоба.' \
                      '\nПример - /balaboba фраза'

BALABOBA_API_ERROR_TEXT = 'Ну это уже перебор. Я не буду дополнять эту фразу.'

BALABOBA_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'

SWEARING_CREATE_MESSAGE = 'Слово "{}" добавлено в базу данных.'
SWEARING_DUPLICATE_ERROR_TEXT = 'Слово "{}" уже есть в базе данных.'
EMPTY_SWEARING_ERROR_TEXT = 'Ты адекватный вообще, нет? Мне что ли пустоту добавить в базу?'
PERMISSION_DENIED_ERROR_TEXT = 'Такому лоху, как ты, нельзя пользоваться этой командой.'

ANSWERS_TO_SWEARING_LIST = [
    'не выражаться!',
    'вот теперь иди и помой рот с мылом!',
    'это тебя в школе таким словам научили?',
]

REMINDER_CREATE_MESSAGE = 'Принял, записал.'
REMINDER_DATE_ERROR = 'Я тебе в прошлое напоминание отправить должен, демон?'
REMINDER_COMMAND_FORMAT_ERROR_TEXT = 'Нихера.' \
                                '\nТут два варианта.' \
                                '\n1. Ты забыл тире между названием задачи и датой напоминания.' \
                                '\n2. Формат даты и времени напоминания неверный.' \
                                '\n\nИспользуй /help, если не в состоянии запомнить пару правил.'

HOLIDAY_GREETING_CREATE_MESSAGE = 'Поздравление создал, я молодец.'
HOLIDAY_GREETING_FORMAT_ERROR_TEXT = 'Пацан, неверный формат команды.'
HOLIDAY_GREETING_DATE_ERROR = 'Я тебе в прошлое поздравление отправить должен, демон?'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = strtobool(os.getenv('EMAIL_USE_TLS'))
EMAIL_SUBJECT = 'Поздравляю! Бота активировали!'

WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid={}'
WEATHER_API_NOT_FOUND_ERROR = 'Дружочек, города "{}" нет на картах.'
WEATHER_API_ERROR = 'Какая-то херня. Пойду разберусь, что у этих синоптиков случилось. Напиши позже.'
WEATHER_EMPTY_CITY_ERROR = 'Ну я не знаю, хоть город укажи. Я тебе что Нострадамус какой-то?'
