from scoutsbevaix.config import TELEGRAM_API_KEY

from telegram import Update
from telegram.ext import Application, MessageHandler, filters


async def handler(update, context):
    msg = update.message
    chat = msg.chat
    date = msg.date
    text = msg.text
    print(
        f"[{date.isoformat()}] {chat.first_name} {chat.last_name} ({chat.id}): {text}")

application = Application.builder().token(TELEGRAM_API_KEY).build()
application.add_handler(MessageHandler(filters.ALL, handler))
application.run_polling(allowed_updates=Update.ALL_TYPES)
