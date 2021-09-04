import random

from asgiref.sync import sync_to_async

from .models import VoiceMessage


@sync_to_async
def get_random_voice_path() -> str:
    """Возвращает путь до случайного голосового сообщения"""
    voices = VoiceMessage.objects.all()
    return random.choice(voices).voice.path
