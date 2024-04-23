import logging
import requests

from constants import (
    API_KEY, 
    API_EVERYTHING_URL, 
    API_TOP_HEADLINES,
    NEWS_PAGE_SIZE,
    LAST_MONTH_DATE
)
import tg_bot.exceptions as exceptions


log = logging.getLogger(__name__)

def log_and_request(url: str, headers:dict):
    """Do GET request to URL and return response."""
    try:
        response = requests.get(url, params=headers)
    except Exception as error:
        log_message = f"Ошибка при запросе к эндпоинту {url}: {error}"
        log.error(log_message, exc_info=True)
        raise exceptions.ConnectionToEndpointError(log_message)
    try:
        response = response.json()
    except Exception as error:
        raise exceptions.DeserializationError(
            f"Ошибка при десериализации запроса {response}: {error}"
        )
    if response["status"] != "ok":
        raise exceptions.ConnectionToEndpointError(
            f"Неверный запрос к эндпоинту: {response}"
            )
    return response

def get_news_by_topic(
    topic: str,
    page: int = 1,
    page_size: int = NEWS_PAGE_SIZE,
    lang: str = "ru") -> dict:
    """Get news by topic."""
    headers = {
        "apiKey": API_KEY,
        "q": topic,
        "searchIm": "title",
        "pageSize": page_size,
        "sortBy": "",
        "from": LAST_MONTH_DATE,
        "language": lang,
        "page": page,
    }
    response = log_and_request(API_EVERYTHING_URL, headers) 
    return response

def get_top_headlines(page:int=1, lang:str="ru") -> dict:
    """Get top-headlines news."""
    headers = {
        "apiKey": API_KEY,
        "country": lang,
        "pageSize": 1,
        "page": page,
    }
    response = log_and_request(API_TOP_HEADLINES, headers)
    return response

def get_news_by_category(category:str, page:int=1, lang:str="ru"):
    """Get news by category."""
    headers = {
        "apiKey": API_KEY,
        "country": lang,
        "pageSize": 1,
        "page": page,
        "category": category,
    }
    response = log_and_request(API_TOP_HEADLINES, headers)
    return response
