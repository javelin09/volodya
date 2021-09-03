import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

HELP_TEXT = 'Здарова, демон.\nИспользуй команду /voice, если хочешь услышать мой бархатный голосок.'
