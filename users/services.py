from asgiref.sync import sync_to_async

from .models import TelegramUser


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
    return created
