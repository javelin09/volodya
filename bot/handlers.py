import asyncio
import random
from datetime import datetime

import aiofiles
from aiogram import types, Dispatcher, Bot
from django.conf import settings
from loguru import logger

from users.services import update_or_create_user
from .services import get_random_voice_path, get_random_sticker_path, get_generated_text


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome_message(message: types.Message):
    """Отправляет приветственное сообщение"""
    await update_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    await message.answer(settings.WELCOME_TEXT)
    logger.info('The welcome message was sent successfully')


@dp.message_handler(commands=['voice'])
async def send_random_voice(message: types.Message):
    """Отправляет случайное голосовое сообщение"""
    path = await get_random_voice_path()
    async with aiofiles.open(path, 'rb') as voice:
        await message.answer_voice(voice)
    logger.info('A voice message was sent successfully')


@dp.message_handler(commands=['flip_coin'])
async def flip_coin(message: types.Message):
    """Отправляет случайный стикер"""
    path = await get_random_sticker_path()
    async with aiofiles.open(path, 'rb') as sticker:
        await message.answer_sticker(sticker)
    logger.info('A sticker was sent successfully')


@dp.message_handler(commands=['balaboba'])
async def send_balaboba_text(message: types.Message):
    """Отправляет дополненный Балабобой текст"""
    phrase = ' '.join(message.text.split()[1:])
    is_empty_phrase, generated_text = await get_generated_text(phrase)
    if is_empty_phrase:
        await message.answer(settings.BALABOBA_COMMAND_ERROR_TEXT)
        logger.info('The balaboba command error message was sent successfully')
    elif not generated_text:
        await message.answer(settings.BALABOBA_API_ERROR_TEXT)
        logger.info('The balaboba api error message was sent successfully')
    else:
        await message.answer(f'*{phrase}*\n\n{generated_text}', parse_mode='markdown')
        logger.info('A generated message was sent successfully')


@dp.message_handler(commands=['remind'])
async def create_remind(message: types.Message):
    """Создает напоминание"""

    async def send_remind(msg: types.Message, delay: float, reminder_text: str):
        """Отправляет напоминание"""
        await asyncio.sleep(delay)
        await msg.reply(reminder_text)
        logger.info('A reminder was sent successfully')
    try:
        text, remind_at = message.text.replace('/remind', '').split('-')
        reminder_delay = (datetime.strptime(remind_at.strip(), '%d.%m.%Y %H:%M') - datetime.now()).total_seconds()
        if reminder_delay < 0:
            await message.reply(settings.REMINDER_DATE_ERROR)
            logger.info('A reminder date is less than the current one')
            return
        asyncio.create_task(send_remind(message, reminder_delay, text.strip()))
        await message.reply(settings.REMINDER_CREATE_MESSAGE)
        logger.info('A reminder was created successfully')
    except ValueError:
        await message.reply(settings.REMINDER_COMMAND_FORMAT_ERROR_TEXT)
        logger.info('The reminder command format error message was sent successfully')


@dp.message_handler(content_types=['text'])
async def reply_to_swearing(message: types.Message):
    """Отвечает на ругательные сообщения"""
    for word in settings.SWEAR_WORDS_LIST:
        if word in message.text.lower():
            reply_text = random.choice(settings.ANSWERS_TO_SWEARING_LIST)
            await message.reply(f'{message.from_user.first_name}, {reply_text}')
            logger.info('A reaction to the swear word was sent successfully')
            break
