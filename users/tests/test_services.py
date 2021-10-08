from django.conf import settings
from django.core import mail

from users.services import send_mail_notification


def test_mail_notification() -> None:
    """Тестирует отправку письма о новом пользователе"""
    send_mail_notification(first_name='Тест', total_users=10)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == settings.EMAIL_SUBJECT
    assert 'Пользователь Тест активировал бота' in mail.outbox[0].body
    assert 'Всего пользователей: 10' in mail.outbox[0].body
