from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




async def build_keyboard(product_num: int, language: str):
    btn_text = "Kursga ro'yxatdan o'tish"
    if language == "ru":
        btn_text = "Зарегистрироваться на курс"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=btn_text, callback_data=f"buy_course:{product_num}")
        ],
    ])
    return markup