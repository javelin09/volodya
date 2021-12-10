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


class HolidayGreeting(models.Model):
    """Поздравления с праздниками"""
    users = models.ManyToManyField(
        'users.TelegramUser',
        verbose_name='Пользователи',
        related_name='holiday_greetings',
    )
    holiday = models.CharField(verbose_name='Название праздника', max_length=50)
    text = models.TextField(verbose_name='Текст поздравления')
    send_on = models.DateTimeField(verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Поздравление с праздниками'
        verbose_name_plural = 'Поздравления с праздниками'
        ordering = ['id']
