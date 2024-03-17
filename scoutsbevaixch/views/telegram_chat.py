import traceback
from django.conf import settings

import telegram


async def send_message_async(message):
    bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)
    for user in settings.TELEGRAM_ALLOWED_USERS:
        try:
            await bot.send_message(chat_id=user["chatId"], text=message)
        except Exception:
            print(traceback.format_exc())
            continue
