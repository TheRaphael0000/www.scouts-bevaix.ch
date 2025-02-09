import traceback
import os

from django.conf import settings
from dotenv import load_dotenv
import telegram

load_dotenv()

async def send_message_async(message):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_API_KEY"))
    for user in settings.TELEGRAM_ALLOWED_USERS:
        try:
            await bot.send_message(chat_id=user["chatId"], text=message)
        except Exception:
            print(traceback.format_exc())
            continue
