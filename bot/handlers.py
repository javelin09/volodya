import asyncio
import random
from datetime import datetime
from typing import Union

import aiofiles
from aiogram.utils.exceptions import ChatNotFound
from aiogram import types, Dispatcher, Bot
from django.conf import settings
from loguru import logger

from users.services import update_or_create_user
from .services import (
    get_random_voice_path,
    get_random_sticker_path,
    get_generated_text,
    is_contains_swearing,
    is_admin,
    add_swear_to_db,
    get_current_weather_data,
    prepare_weather_forecast,
    get_all_telegram_user_ids,
)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome_message(message: types.Message):
    """Отправляет приветственное сообщение"""
    created = await update_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    if created:
        logger.success(f'The user with id={message.from_user.id} was created successfully')
    await message.answer(settings.WELCOME_TEXT)
    logger.success('The welcome message was sent successfully')


@dp.message_handler(commands=['voice'])
async def send_random_voice(message: types.Message):
    """Отправляет случайное голосовое сообщение"""
    path = await get_random_voice_path()
    async with aiofiles.open(path, 'rb') as voice:
        await message.answer_voice(voice)
    logger.success('A voice message was sent successfully')


@dp.message_handler(commands=['flip_coin'])
async def flip_coin(message: types.Message):
    """Отправляет случайный стикер"""
    path = await get_random_sticker_path()
    async with aiofiles.open(path, 'rb') as sticker:
        await message.answer_sticker(sticker)
    logger.success('A sticker was sent successfully')


@dp.message_handler(commands=['balaboba'])
async def send_balaboba_text(message: types.Message):
    """Отправляет дополненный Балабобой текст"""
    phrase = ' '.join(message.text.split()[1:])
    is_empty_phrase, generated_text = await get_generated_text(phrase)
    if is_empty_phrase:
        await message.reply(settings.BALABOBA_COMMAND_ERROR_TEXT)
    elif not generated_text:
        await message.reply(settings.BALABOBA_API_ERROR_TEXT)
    else:
        await message.answer(f'*{phrase}*\n\n{generated_text}', parse_mode='markdown')
        logger.success('A generated message was sent successfully')


@dp.message_handler(commands=['remind'])
async def create_reminder(message: types.Message):
    """Создает напоминание"""

    async def send_reminder(msg: types.Message, delay: float, reminder_text: str):
        """Отправляет напоминание"""
        await asyncio.sleep(delay)
        await msg.reply(reminder_text)
        logger.success('A reminder was sent successfully')

    try:
        text, remind_at = message.text.replace('/remind', '').split('-')
        reminder_delay = (datetime.strptime(remind_at.strip(), '%d.%m.%Y %H:%M') - datetime.now()).total_seconds()
        if reminder_delay < 0:
            await message.reply(settings.REMINDER_DATE_ERROR)
            return
        asyncio.create_task(send_reminder(message, reminder_delay, text.strip()))
        await message.reply(settings.REMINDER_CREATE_MESSAGE)
        logger.success('A reminder was created successfully')
    except ValueError:
        await message.reply(settings.REMINDER_COMMAND_FORMAT_ERROR_TEXT)


@dp.message_handler(commands=['add_swear'])
async def add_swear(message: types.Message):
    """Добавляет ругательное слово в БД (доступно только админам)"""
    swear = message.text.replace('/add_swear', '').strip().lower()
    if not swear:
        await message.reply(settings.EMPTY_SWEARING_ERROR_TEXT)
        return
    if await is_admin(message.from_user.id):
        created = await add_swear_to_db(swear)
        if created:
            await message.reply(settings.SWEARING_CREATE_MESSAGE.format(swear))
            logger.success('A swear word was successfully added to the database')
        else:
            await message.reply(settings.SWEARING_DUPLICATE_ERROR_TEXT.format(swear))
    else:
        await message.reply(settings.PERMISSION_DENIED_ERROR_TEXT)


@dp.message_handler(commands=['weather'])
async def send_forecast(message: types.Message):
    """Отправляет прогноз погоды в указанном городе"""
    city_name = message.text.replace('/weather', '').strip().lower()
    if not city_name:
        await message.reply(settings.WEATHER_EMPTY_CITY_ERROR)
        return
    weather_data = await get_current_weather_data(city_name)
    if int(weather_data['cod']) == 404:
        await message.reply(settings.WEATHER_API_NOT_FOUND_ERROR.format(city_name))
        return
    if int(weather_data['cod']) != 200:
        await message.reply(settings.WEATHER_API_ERROR)
        return
    forecast = await prepare_weather_forecast(weather_data)
    await message.answer(forecast, parse_mode='markdown')
    logger.success('The weather forecast was sent successfully')


@dp.message_handler(commands=['holiday_greeting'])
async def create_holiday_greeting(message: types.Message):
    """Создает праздничное поздравление"""

    async def send_holiday_greeting(
        greeting_text: str,
        send_to_user: Union[str, int],
        delay: float,
    ):
        """Отправляет праздничное поздравление"""
        await asyncio.sleep(delay)
        try:
            if send_to_user == 'all':
                for telegram_id in await get_all_telegram_user_ids():
                    await bot.send_message(telegram_id, greeting_text)
            else:
                await bot.send_message(send_to_user, greeting_text)
        except ChatNotFound:
            logger.info(f'Some users stopped the bot. Skipping...')
        logger.success('A greeting was sent successfully')

    if not await is_admin(message.from_user.id):
        await message.reply(settings.PERMISSION_DENIED_ERROR_TEXT)
        return
    try:
        items = message.text.replace('/holiday_greeting', '').split('-')
        text, send_at, send_to = [item.strip() for item in items]
        greeting_delay = (
                datetime.strptime(send_at.strip(), '%d.%m.%Y %H:%M') - datetime.now()
        ).total_seconds()
        if greeting_delay < 0:
            await message.reply(settings.HOLIDAY_GREETING_DATE_ERROR)
            return
        asyncio.create_task(send_holiday_greeting(text, send_to, greeting_delay))
        await message.reply(settings.HOLIDAY_GREETING_CREATE_MESSAGE)
        logger.success('A greeting was created successfully')
    except ValueError:
        await message.reply(settings.HOLIDAY_GREETING_FORMAT_ERROR_TEXT)


@dp.message_handler(content_types=['text'])
async def reply_to_swearing(message: types.Message):
    """Отвечает на ругательные сообщения"""
    if (
        await is_contains_swearing(message.text)
        and not await is_admin(message.from_user.id)
    ):
        reply_text = random.choice(settings.ANSWERS_TO_SWEARING_LIST)
        await message.reply(f'{message.from_user.first_name}, {reply_text}')
        logger.success('A reaction to the swear word was sent successfully')
