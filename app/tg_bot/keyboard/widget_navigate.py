from telegram import InlineKeyboardButton

from constants import NEWS_CATEGORIES

def widget_buttons_navigate_logic(
        page_count:int, 
        page:int, 
        source:str, 
        topic:str
        )-> list:
    """Return list buttons depending on user is on page."""
    if page == 1 and page != page_count:
        reply_keyboard = [
            [InlineKeyboardButton(
                "Вперед", 
                callback_data=f"{source},Next,{topic},{page}"
                )
             ],
            [InlineKeyboardButton(
                "Удалить виджет", 
                callback_data=f"delete_widget"
                )
             ],
        ]
    elif page_count == page and page_count != 1:
        reply_keyboard = [
            [InlineKeyboardButton(
                "Назад", 
                callback_data=f"{source},Previous,{topic},{page}"
                ),
             ],
            [InlineKeyboardButton(
                "Удалить виджет",
                callback_data=f"delete_widget"
                )
             ],
        ]
    elif page_count == page and page == 1:
        reply_keyboard = [
            [InlineKeyboardButton(
                "Удалить виджет",
                callback_data=f"delete_widget"
                )
             ],
        ]
    else:
        reply_keyboard = [
            [InlineKeyboardButton("Назад", callback_data=f"{source},Previous,{topic},{page}"),
             InlineKeyboardButton("Вперед", callback_data=f"{source},Next,{topic},{page}")],
            [InlineKeyboardButton(
                "Удалить виджет", 
                callback_data=f"delete_widget"
                )
             ],
    ]
    return reply_keyboard

def list_of_all_categories():
    reply_keyboard = []
    for category, name in NEWS_CATEGORIES.items():
        reply_keyboard.append(
            [InlineKeyboardButton(
                name, 
                callback_data=f"categories_widget,{category}"
                )]
        )
    return reply_keyboard