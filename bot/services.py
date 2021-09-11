import ast
import json
import random
import urllib.request

from asgiref.sync import sync_to_async
from django.conf import settings

from .models import VoiceMessage, Sticker, SwearWord


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
    return telegram_user_id == settings.TELEGRAM_ADMIN_ID


@sync_to_async
def add_swear_to_db(swear: str) -> bool:
    """Добавляет ругательное слово в БД"""
    _, created = SwearWord.objects.filter(word=swear).update_or_create(defaults={'word': swear})
    return created
