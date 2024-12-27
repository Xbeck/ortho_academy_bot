from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




language_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text="🇷🇺 ", callback_data="language,ru"),
        InlineKeyboardButton(text="🇺🇿 ", callback_data="language,uz")
        ]])