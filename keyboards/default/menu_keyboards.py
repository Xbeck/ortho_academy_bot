from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




# --------------- Admin keyboards ----------------------------
async def admin_panel_btn(language=None):
    btn_text_1 = "👤 Obunachilar"
    btn_text_2 = "📖 Kurslar"
    # btn_text_3 = "💭 E'lon yo'llash"
    # btn_text_4 = "🇺🇿 Til"

    if language == "ru":
        btn_text_1 = "👤 Подписчики"
        btn_text_2 = "📖 Курсы"
        # btn_text_3 = "💭 Объявление"
        # btn_text_4 = "🇷🇺 Язык"

    murkap = ReplyKeyboardMarkup(
    keyboard=[
                [KeyboardButton(text=btn_text_1)],
                [KeyboardButton(text=btn_text_2)]
                # [
                #  KeyboardButton(text=btn_text_3),
                #  KeyboardButton(text=btn_text_4)
                #  ],

                 ],
    resize_keyboard=True)
    return murkap


#---------------------- User panel keyboards ----------------------
async def user_panel_btn(language=None):
    btn_text_1 = "📒 Kurslar"  # 🎫🎟📒
    btn_text_2 = "🛍 Market"   # ⭐️🌟✨⚡️
    # btn_text_3 = "🇺🇿 Til"
    btn_text_4 = "❕ help"
    
    if language == "ru":
        btn_text_1 = "📒 Курсы"
        btn_text_2 = "🛍 Market"
        # btn_text_3 = "🇷🇺 Язык"
        btn_text_4 = "❕ Помощь"

    murkap = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn_text_1)],
            [KeyboardButton(text=btn_text_2)],
            # [
            #     # KeyboardButton(text=btn_text_3),
            #     KeyboardButton(text=btn_text_4)
            #  ],
            ],
        resize_keyboard=True)
    return murkap

