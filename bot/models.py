import os

from django.db import models


class VoiceMessage(models.Model):
    """Голосовые сообщения"""
    voice = models.FileField(verbose_name='Голосовое сообщение', upload_to='voices')

    @property
    def file_name(self):
        return os.path.basename(self.voice.name)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Голосовое сообщение'
        verbose_name_plural = 'Голосовые сообщения'
        ordering = ['id']


class Sticker(models.Model):
    """Стикеры"""
    sticker = models.FileField(verbose_name='Стикеры', upload_to='stickers')

    @property
    def file_name(self):
        return os.path.basename(self.sticker.name)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Стикер'
        verbose_name_plural = 'Стикеры'
        ordering = ['id']


class SwearWord(models.Model):
    """Ругательные слова"""
    word = models.CharField(max_length=50, verbose_name='Ругательное слово')

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Ругательное слово'
        verbose_name_plural = 'Ругательные слова'
        ordering = ['id']
