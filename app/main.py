import sys
import logging

from telegram import Update
from telegram.ext import (
    filters, 
    ApplicationBuilder, 
    MessageHandler, 
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
)

from tg_bot.commands import start, help
from tg_bot.services import (
    send_news,
    callback_handler,
    send_top_headlines,
    send_list_of_all_categories_widget,
    send_news_by_category,
)
from constants import BOT_TOKEN, API_KEY
from database.queries import create_tables
from tg_bot.inline_handlers import send_news_on_the_topic_inline

log = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        filename=f"./logs/{__name__}.log",
        filemode="w",
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

def check_constants():
    """Checking the env constants."""
    if BOT_TOKEN and API_KEY:
        return True
    log.critical("Required env variables not found")
    return False

def main():
    log.info("Start programm")
    const_checker = check_constants()
    if not const_checker:
        sys.exit("Requierd environment variables not found")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    all_messages_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        send_news
        )
    top_headlines_handler = MessageHandler(
        filters.Regex("^Топ новостей$"),
        send_top_headlines
        )
    news_by_category_handler = MessageHandler(
        filters.Regex("^Новости (спорта|медицины|технологий"
                          "|науки|развлечений|бизнеса)$"),
        send_news_by_category
        )
    categories_list = MessageHandler(
        filters.Regex("^Новости на тему$"),
        send_list_of_all_categories_widget
        )
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    application.add_handler(start_handler)
    application.add_handler(help_handler) 
    application.add_handler(top_headlines_handler)
    application.add_handler(categories_list)
    application.add_handler(news_by_category_handler)
    application.add_handler(all_messages_handler)
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(InlineQueryHandler(send_news_on_the_topic_inline))
    application.run_polling()


if __name__ == '__main__':
   main()
