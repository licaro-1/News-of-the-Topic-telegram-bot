from telegram import InlineKeyboardButton

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
             InlineKeyboardButton("Вперед", callback_data=f"{source},Next,{topic},{page}")
             ],
            [InlineKeyboardButton(
                "Удалить виджет", 
                callback_data=f"delete_widget"
                )
             ],
    ]
    return reply_keyboard