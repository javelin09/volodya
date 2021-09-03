import os
import random


def get_file_name() -> str:
    """Возвращает имя случайного аудиофайла в директории voices"""
    voices = os.listdir('voices')
    files_number = len(voices) - 1
    random_number = random.randint(0, files_number)
    return voices[random_number]
