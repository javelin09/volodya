from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import HolidayGreeting


@receiver(post_save, sender=HolidayGreeting)
def send_holiday_greeting_signal(sender, instance, created, **kwargs):
    """Отправляет поздравление с праздником после его сохранения"""
    pass
