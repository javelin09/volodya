import ast
import json
import random
import urllib.request

from asgiref.sync import sync_to_async
from django.conf import settings

from .models import VoiceMessage, Sticker


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
