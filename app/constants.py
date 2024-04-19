import os

from dotenv import load_dotenv
from datetime import date, timedelta


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

LAST_MONTH_DATE = date.today() - timedelta(days=29)

API_EVERYTHING_URL = "https://newsapi.org/v2/everything"
API_TOP_HEADLINES = "https://newsapi.org/v2/top-headlines"

NEWS_AVATAR_URL = "https://telegra.ph/file/842d1c31ce4df0a80b251.png"
BOT_AVATAR_URL = "https://telegra.ph/file/a866525fed5aae3416b4e.png"

NEWS_PAGE_SIZE = 1
INLINE_NEWS_COUNT = 50

NEWS_CATEGORIES = {
    "business": "Бизнес",
    "science": "Наука",
    "sports": "Спорт",
    "technology": "Технологии",
    "entertainment": "Развлечения",
    "health": "Медицина",
    }

MESSAGE_TO_NEWS_CATEGORY = {
    "новости бизнеса": "business",
    "новости науки": "science",
    "новости спорта": "sports",
    "новости технологий": "technology",
    "новости развлечений": "entertainment",
    "новости медицины": "health",
    }


IMG_BY_CATEGORY = {
        "science": "https://telegra.ph/file/076781672868700a2d13e.jpg",
        "business": "https://telegra.ph/file/9dac74a2e19b18fe2db86.jpg",
        "health": "https://telegra.ph/file/80441c97116e7d3ea701b.jpg",
        "entertainment": "https://telegra.ph/file/d89e7c8b8e79ef9712e88.jpg",
        "sports": "https://telegra.ph/file/3a69c569a225fa6235900.jpg",
        "technology": "https://telegra.ph/file/afa1582831313c107d5f9.jpg",
        "top_headlines": "https://telegra.ph/file/7d84ec74db26645374c7b.jpg",
    }

TEMPLATE_MESSAGES = {
    "start":("Привет! Я новостной бот.\nНапиши тему и я найду новости по ней"
             "\n\nВведите /help чтобы узнать больше возможностей"),
    "help": ("Новостной бот News of the Topic предназначен для " 
            "просмотра новостей со всего мира.\n\nОтправьте тему и бот " 
             "покажет найденные по ней новости.\n\nОтправьте фразу "
             "<u><i>Топ новостей</i></u> и бот отправит вам топ новостей "
             "за последнюю неделю"
             "\n\nОтправьте боту фразу <u><i>Новости на тему</i></u> или "
             "<u><i>Новости (медицины,спорта,развлечений,бизнеса или технологий)</i></u>, "
             "чтобы выбрать определенную категорию новостей"
             "\n\nИспользуйте кнопку под сообщением для " 
             "навигации в виджете\n\nYour developer - licaro-1:https://github.com/licaro-1"),
    "no_news":("<b>Не нашел новостей на указанную тему</b>"
               "\n\nУбедитесь в правильности ввода или введите "
               "/help чтобы узнать возможности бота"),
    "select_category": ("<b>Выберите категорию</b>"),
    "about_bot": ("Привет! Я новостной бот News of the Topic"
                "\n\nНапиши мне чтобы получить актуальные "
                "новости на указанную тему или топ новостей "
                "за последний месяц\nТакже я могу отсортировать "
                "новости по выбранной категории."),
}
