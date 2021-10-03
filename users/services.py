from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import TelegramUser


def send_mail_notification(first_name, total_users):
    """Отправляет письмо админу о новом пользователе"""
    context = {
        'first_name': first_name,
        'total_users': total_users,
    }
    html_message = render_to_string('mail_notification.html', context)
    send_mail(
        subject=settings.EMAIL_SUBJECT,
        message=strip_tags(html_message),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
        html_message=html_message,
    )


@sync_to_async
def update_or_create_user(
        telegram_id: int,
        username: str,
        first_name: str,
        last_name: str,
) -> None:
    """Обновляет/создает пользователя в БД"""
    defaults = {
        'telegram_id': telegram_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
    }
    _, created = TelegramUser.objects.filter(telegram_id=telegram_id).update_or_create(defaults=defaults)
    if created:
        total_users = TelegramUser.objects.count()
        send_mail_notification(first_name, total_users)
    return created
