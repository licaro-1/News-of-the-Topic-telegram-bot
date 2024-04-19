import logging

from uuid import uuid4
from telegram import (
        InlineQueryResultPhoto, 
        Update,
        InlineQueryResultArticle,
        InputTextMessageContent
        )
from telegram.ext import ContextTypes

from api_news.get_news import get_news_by_topic
from tg_bot.services import post_formatter
from tg_bot.to_prettier import to_prettier_all_news
from constants import (
    BOT_AVATAR_URL, 
    TEMPLATE_MESSAGES,
    INLINE_NEWS_COUNT
)

log = logging.getLogger(__name__)

async def send_news_on_the_topic_inline(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send news list on the topic in inline mode."""
    query = update.inline_query.query
    news_response = get_news_by_topic(query,page_size=INLINE_NEWS_COUNT)
    log.info(f"Start inline func, user_query: {query}")
    news = news_response.get("articles")
    if not query or not news:
        return
    results = []
    for post in news:
        news_to_format = post_formatter(post)
        title, description, post_url, image_url = (
        news_to_format.get("title"), 
        news_to_format.get("description"),
        news_to_format.get("post_url"), 
        news_to_format.get("image_url")
    )
        caption = to_prettier_all_news(title, description, post_url)
        results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url=image_url,
            thumbnail_url=image_url,
            caption=caption,
            title=title,
            description=description[:200],
            parse_mode="html",
        ))
    results.append(InlineQueryResultArticle(
            id=str(uuid4()),
            thumbnail_url=BOT_AVATAR_URL,
            title="News of the Topic",
            description="Write me to get more news",
            input_message_content=InputTextMessageContent(
                TEMPLATE_MESSAGES["about_bot"]),
        ))
    log.info(f"return inline query to user: "
            f"{update.inline_query.from_user.id} query: {query}")
    await update.inline_query.answer(results) 
 
    

