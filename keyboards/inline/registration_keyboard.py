from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# local moduls
from functions.all_functions import message_fillter




async def register_btn(language):
    btn_text = await message_fillter(language,
                                "Зарегистрироваться",
                                "Ro'yxatdan o'tish")
    callback_text = "register,uz"

    if language == "ru":
        callback_text = "register,ru"
    
    markup = InlineKeyboardMarkup(
                                    inline_keyboard=[[InlineKeyboardButton(text=btn_text,
                                                                           callback_data=callback_text)]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return markup