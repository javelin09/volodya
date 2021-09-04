from aiogram import executor
from django.core.management.base import BaseCommand
from loguru import logger

from bot.handlers import dp


class Command(BaseCommand):
    """Менеджмент команда по запуску телеграм бота"""
    help = 'Start the telegram bot'

    def handle(self, *args, **kwargs):
        logger.info('Ooh yeah! Volodya is started!')
        executor.start_polling(dp, skip_updates=True)
