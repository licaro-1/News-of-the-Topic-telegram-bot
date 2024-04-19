import logging
from telegram import Update
from telegram.ext import ContextTypes

from constants import TEMPLATE_MESSAGES
from database.queries import create_user

log = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler."""
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    await create_user(username, telegram_id)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = TEMPLATE_MESSAGES.get("start"))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help command handler."""
    await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = TEMPLATE_MESSAGES.get("help"),
            parse_mode="html")


