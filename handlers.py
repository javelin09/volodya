import aiofiles
from aiogram import types, Dispatcher, Bot

from config import HELP_TEXT, BOT_TOKEN
from services import get_random_file_name

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome_message(message: types.Message):
    """Отправляет приветственное сообщение"""
    await message.answer(HELP_TEXT)


@dp.message_handler(commands=['voice'])
async def send_random_voice(message: types.Message):
    """Отправляет случайное голосовое сообщение"""
    file_name = get_random_file_name()
    async with aiofiles.open(f'voices/{file_name}', 'rb') as voice:
        await message.answer_voice(voice)
