import ast
import json
import random
import urllib.request

import requests
from asgiref.sync import sync_to_async
from django.conf import settings

from .models import VoiceMessage, Sticker, SwearWord
from users.models import TelegramUser


@sync_to_async
def get_random_voice_path() -> str:
    """Возвращает путь до случайного голосового сообщения"""
    voices = VoiceMessage.objects.all()
    return random.choice(voices).voice.path


@sync_to_async
def get_random_sticker_path() -> str:
    """Возвращает путь до случайного стикера"""
    stickers = Sticker.objects.all()
    return random.choice(stickers).sticker.path


@sync_to_async
def get_generated_text(phrase: str) -> tuple:
    """Возвращает дополненный Балабобой текст"""
    is_empty_phrase = False
    if not phrase:
        is_empty_phrase = True
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'query': phrase,
        'intro': 4,  # у пацанских цитат стиль 4
        'filter': 1,
    }
    data = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(settings.BALABOBA_URL, data=data, headers=headers)
    response_binary = urllib.request.urlopen(req).read().decode('utf-8')
    generated_text = ast.literal_eval(response_binary)
    return is_empty_phrase, generated_text['text']


@sync_to_async
def is_contains_swearing(message: str) -> bool:
    """Проверяет сообщение на наличие ругательных слов"""
    swearing_list = SwearWord.objects.all()
    for swearing in swearing_list:
        if swearing.word in message.lower():
            return True
    return False


@sync_to_async
def is_admin(telegram_user_id: int) -> bool:
    """Проверяет, является ли пользователь админом"""
    return TelegramUser.objects.get(telegram_id=telegram_user_id).is_admin


@sync_to_async
def add_swear_to_db(swear: str) -> bool:
    """Добавляет ругательное слово в БД"""
    _, created = SwearWord.objects.filter(word=swear).update_or_create(defaults={'word': swear})
    return created


@sync_to_async
def get_current_weather_data(city_name: str) -> dict:
    """Возвращает прогноз погоды от OpenWeatherMap"""
    url = settings.WEATHER_API_URL.format(city_name, settings.WEATHER_API_TOKEN)
    response = requests.get(url).json()
    return response


@sync_to_async
def prepare_weather_forecast(weather_data: dict) -> str:
    """Подготавливает прогноз к отправке пользователю"""
    weather_descriptions = []
    weather_main = []
    for weather in weather_data['weather']:
        weather_descriptions.append(weather['description'])
        weather_main.append(weather['main'])
    forecast = f"*Прогноз погоды в городе {weather_data['name']}*\n\n" \
               f"За окном {', '.join(weather_descriptions)}\n" \
               f"Температура: {round(weather_data['main']['temp'])}°C\n" \
               f"Ощущается как: {round(weather_data['main']['feels_like'])}°C\n" \
               f"Влажность: {round(weather_data['main']['humidity'])}%\n" \
               f"Скорость ветра: {round(weather_data['wind']['speed'])} м/c"
    if round(weather_data['main']['temp']) < 0:
        forecast += '\n\nЯ бы советовал одеться потеплее.'
    if -10 > round(weather_data['main']['temp']) > -50:
        forecast += '\n\nТочнее без подштанников я бы не выходил!'
    if round(weather_data['main']['temp']) > 30:
        forecast += '\n\nЛето, плавки, рок-н-ролл.'
    if 'Rain' in weather_main:
        forecast += '\n\nНе забудь зонт.'
    return forecast
