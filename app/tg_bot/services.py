import logging
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    InputMediaPhoto,
    )
from telegram.ext import ContextTypes

from api_news.get_news import (
    get_news_by_topic,
    get_top_headlines,
    get_news_by_category,
)
from constants import (
    NEWS_CATEGORIES,
    TEMPLATE_MESSAGES,
    MESSAGE_TO_NEWS_CATEGORY,
    IMG_BY_CATEGORY,
)
from tg_bot.to_prettier import (
    to_prettier_all_news,
    to_prettier_top_headlines,
    to_prettier_news_by_category,
    post_formatter
)
from database.queries import (
    create_user, 
    update_messages_count, 
    update_nav_moves_count
)
from tg_bot.keyboard.widget_navigate import widget_buttons_navigate_logic
import tg_bot.exceptions as exceptions


log = logging.getLogger(__name__)

CALLBACK_TYPE_TO_FUNC = {
    "all_news": get_news_by_topic,
    "top_headlines": get_top_headlines,
    "categories": get_news_by_category,
}

async def no_news_on_the_topic(
        chat_id:int, 
        context: ContextTypes.DEFAULT_TYPE
        ):
    try:
        await context.bot.send_message(
                chat_id=chat_id,
                text=TEMPLATE_MESSAGES["no_news"],
                parse_mode="html"
            )
    except Exception as error:
        raise exceptions.SendMessageError(f"{error}")

async def send_news_to_user(
        context:ContextTypes.DEFAULT_TYPE, 
        **kwargs
        ):
    """Send photo message to user."""
    try:
        log.info(f"Start send news to user: {kwargs.get('chat_id')}")
        await context.bot.send_photo(**kwargs)
        log.info("News send succesfull")
    except Exception as error:
        log_message = (f"Ошибка при попытке отправить" 
                        f" сообщение, {kwargs}, {error}")
        log.error(log_message, exc_info=True)
        raise exceptions.SendMessageError(error)

async def change_media_message(query, image, **kwargs):
    """Change message by bot when user got swap in widget."""
    try:
        await query.edit_message_media(image)
        await query.edit_message_caption(**kwargs)
        log.info("Message change succesfull")
    except Exception as error:
        log.warning("Erorr accepting message change")
        raise exceptions.ChangeMediaMessageError(error)

async def delete_news_widget(query):
    """Delete news widget."""
    await query.delete_message()

async def callback_handler(
        update: Update, 
        context:ContextTypes.DEFAULT_TYPE
        ):
    """Callback handler."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception as error:
        raise exceptions.CallbackQueryAnswerError(
            f"CallbackQueryAnswerError: {error}"
            )
    callback_type = query.data.split(',')[0]
    if callback_type == "delete_widget":
        return await delete_news_widget(query)
    if callback_type in "all_news,top_headlines,categories":
        telegram_id = update.callback_query.message.chat.id
        await update_nav_moves_count(telegram_id)
        return await news_navigation_button_handler(callback_type, query)
    elif callback_type == "categories_widget":
        category = query.data.split(',')[1]
        return await send_news_by_category(update, context, category)

async def news_navigation_button_handler(
        callback_type: str,
        query) -> None:
    _, step, topic, page = query.data.split(',')
    page = int(page)
    if step == "Next":
        page += 1
    else:
        page -= 1
    if topic != " ":
        response = CALLBACK_TYPE_TO_FUNC[callback_type](topic, page)
    else:
        response = CALLBACK_TYPE_TO_FUNC[callback_type](page) 
    news = post_formatter(response.get("articles")[0])
    title, description, post_url, image = (
        news.get("title"),
        news.get("description"),
        news.get("post_url"),
        news.get("image_url"),
    )
    image = InputMediaPhoto(news.get("image_url"))
    if callback_type == "all_news":
        caption = to_prettier_all_news(title, description, post_url)
    elif callback_type == "top_headlines":
        caption = to_prettier_top_headlines(title, post_url)
    elif callback_type == "categories":
        caption = to_prettier_news_by_category(topic, title, post_url)
        image = InputMediaPhoto(IMG_BY_CATEGORY[topic])
    total_pages = response.get("totalResults")
    reply_keyboard = widget_buttons_navigate_logic(
            total_pages, 
            page, 
            callback_type, 
            topic
        )
    await change_media_message(
            query=query,
            image=image,
            caption=caption, 
            parse_mode="html", 
            reply_markup=InlineKeyboardMarkup(reply_keyboard))

async def send_news(
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE,
        page: int = 1
        ) -> None:
    """Get Topic, wait answer API News for the news, send news to user."""
    topic = update.message.text
    chat_id = update.effective_chat.id
    news_response = get_news_by_topic(topic, page)
    news =  news_response.get("articles")
    if not news:
        return await no_news_on_the_topic(chat_id, context)
    news = post_formatter(news[0])
    title, post_url, description, page_count, image = (
        news.get("title"), 
        news.get("post_url"),
        news.get("description"), 
        news.get("page_count"),
        news.get("image_url"),
    )
    caption = to_prettier_all_news(
        title,
        description,
        post_url
    )
    reply_keyboard = widget_buttons_navigate_logic(
        page_count, 
        page,
        "all_news", 
        topic,
    )
    telegram_id = update.message.from_user.id
    await update_messages_count(telegram_id)
    await send_news_to_user(
            context,
            chat_id=update.effective_chat.id, 
            caption=caption,
            parse_mode="html",
            photo=image,
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
         )

async def send_top_headlines(
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE, 
        page: int = 1):
    """Get news in the top headlines and send to user."""
    chat_id = update.effective_chat.id
    news_response = get_top_headlines(page)
    news = news_response.get("articles")
    if not news:
        return await no_news_on_the_topic(chat_id, context)
    news = post_formatter(news[0])
    title, post_url, image, page_count = (
        news.get("title"), 
        news.get("post_url"),
        news.get("image_url"),
        news.get("page_count")
    )
    caption = to_prettier_top_headlines(
            title, post_url)
    reply_keyboard = widget_buttons_navigate_logic(
        page_count, 
        page,
        "top_headlines", 
        " ",
    )
    telegram_id = update.message.from_user.id
    await update_messages_count(telegram_id)
    await send_news_to_user(
            context,
            chat_id=update.effective_chat.id, 
            caption=caption,
            parse_mode="html",
            photo=image,
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
         )

async def send_list_of_all_categories_widget(
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
        ):
    """Send widget with all categories."""
    reply_keyboard = []
    for category, name in NEWS_CATEGORIES.items():
        reply_keyboard.append(
            [InlineKeyboardButton(
                name, 
                callback_data=f"categories_widget,{category}"
                )]
        )
    telegram_id = update.message.from_user.id
    await update_messages_count(telegram_id)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = TEMPLATE_MESSAGES.get("select_category"),
        reply_markup = InlineKeyboardMarkup(reply_keyboard),
        parse_mode="html")

async def send_news_by_category(
        update:Update,
        context: ContextTypes.DEFAULT_TYPE,
        category: str = None,
        page: int = 1):
    """Send news by category."""
    chat_id = update.effective_chat.id
    if not category and update.message.text:
        user_message = update.message.text.lower()
        if user_message in MESSAGE_TO_NEWS_CATEGORY.keys():
            category = MESSAGE_TO_NEWS_CATEGORY[user_message]
        else:
            return
    log.info("Start send news by category")
    news_response = get_news_by_category(category, page)
    news = news_response.get("articles")
    if not news:
        return await no_news_on_the_topic(chat_id, context)
    news = post_formatter(news[0])
    title, post_url, page_count = (
        news.get("title"), 
        news.get("post_url"), 
        news.get("page_count")
    )
    image = IMG_BY_CATEGORY[category]
    caption = to_prettier_news_by_category(category, title, post_url)
    reply_keyboard = widget_buttons_navigate_logic(
        page_count, 
        page,
        "categories", 
        category,
    )
    await update_messages_count(chat_id)
    await send_news_to_user(
            context,
            chat_id=chat_id,
            caption=caption,
            parse_mode="html",
            photo=image,
            reply_markup=InlineKeyboardMarkup(reply_keyboard),
        )
