from django.db import models


class TelegramUser(models.Model):
    """Пользователи в телеграме"""
    telegram_id = models.PositiveIntegerField(verbose_name='ID пользователя в телеграме', unique=True)
    username = models.CharField(max_length=50, verbose_name='Имя пользователя', null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', null=True, blank=True)
    is_admin = models.BooleanField(verbose_name='Администратор', default=False)

    def __str__(self):
        return self.first_name or str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь в телеграме'
        verbose_name_plural = 'Пользователи в телеграме'
        ordering = ['id']
