from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



async def check_button(language=None):
    btn_text = "Obunani tekshirish"
    if language == "ru":
        btn_text = "Проверить подписку"

    
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=btn_text, callback_data="check_subs")
            ]
        ]
    )
    return markup