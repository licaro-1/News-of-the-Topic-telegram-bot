from constants import NEWS_CATEGORIES, NEWS_AVATAR_URL

def to_prettier_all_news(title:str, description:str, url:str) -> str:
    """Format news to prettier view."""
    return f"<a href='{url}'><b>{title}</b></a>\n\n{description}"

def to_prettier_top_headlines(title:str, url:str) -> str:
    """Format top-headlines news to prettier view."""
    return (
        f"<u><i>Топ новостей за последнюю неделю:</i></u>"
        f"\n\n<a href='{url}'><b>{title}</b></a>"
        )

def to_prettier_news_by_category(category:str, title:str, url:str) -> str:
    """Format news by categories to prettier view."""
    return (
        f"<b><i>Новости на тему <u>{NEWS_CATEGORIES[category]}</u>:</i></b>"
        f"\n\n<a href='{url}'><b>{title}</b></a>"
        )

def post_formatter(news:dict) -> dict:
    """Get json dict of response API ang change img to default if doesnt exists."""
    news_with_tags = {
    "title": news.get('title'),
    "image_url": news.get("urlToImage"),
    "description": news.get("description"),
    "post_url": news.get('url'),
    }
    if not news_with_tags["image_url"]:
        news_with_tags["image_url"] = NEWS_AVATAR_URL
    return news_with_tags


