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
