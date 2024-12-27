import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton







# # Market products btns
# async def products_menu_btn(language=None):
#     logging.info("products menu btn")
#     from loader import db

#     # DB dan products objectini olish
#     try:
#         products_objs = await db.select_products()
#     except Exception as e:
#         logging.info(e)
#         products_objs = None

#     logging.info("test 1")
#     markup = InlineKeyboardMarkup(row_width=1)
#     if products_objs:
#         for i, product in enumerate(products_objs):
#             btn_text = product['name']
#             btn_text_1 = "🛒" # 🛒🛍
#             btn_text_2 = "↩️ Ortga"
#             callback_text = f"products_info,{product['id']}"

#             if language == "ru":
#                 btn_text = product['name']
#                 btn_text_1 = "🛒"
#                 btn_text_2 = "↩️ Назад"
#             markup.insert(InlineKeyboardButton(text=btn_text, callback_data=callback_text))
        
#         callback_text_1 = f"finish"
#         callback_text_2 = "_back_0"
#         markup.insert(InlineKeyboardButton(text=btn_text_1, callback_data=callback_text_1))
#         markup.insert(InlineKeyboardButton(text=btn_text_2, callback_data=callback_text_2))
#     return markup


# Product info btns
async def product_info_btn(product_num: int, language=None, callback=None):
    logging.info("products info btn")
    from loader import db 

    count = 1
    if callback:
        count = callback
    else:
        pass

    # DB dan products objectini olish
    try:
        product_obj = await db.select_one_product(product_num)
    except Exception as e:
        logging.info(e)
        product_obj = None

    # markup = InlineKeyboardMarkup(row_width=3)
    if product_obj:
        button_text_1 = "<< Oldingi"
        button_text_2 = "-"
        button_text_3 = f"{count} dona"
        button_text_4 = "+"
        button_text_5 = "Keyingi >>"
        button_text_6 = "Xarid qilish"
        button_text_7 = "🛒"
        button_text_8 = "↩️ Ortga"

        if language == "ru":
            button_text_1 = "<< Предыдущий"
            button_text_2 = "-"
            button_text_3 = f"{count} шт"
            button_text_4 = "+"
            button_text_5 = "Следующий >>"
            button_text_6 = "Купить"
            button_text_7 = "🛒"
            button_text_8 = "↩️ Назад"

        # callback_text = f"product_basket,{product_obj['id']}"
        # callback_text_1 = ""
        callback_text_8 = "_back_0"

        markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text=button_text_1, callback_data=f"_previous,{product_num},{count}"),
                            InlineKeyboardButton(text=button_text_5, callback_data=f"_next,{product_num},{count}")
                            ],
                        [
                            InlineKeyboardButton(text=button_text_2, callback_data=f"decr,_count,{product_num},{count}"),
                            InlineKeyboardButton(text=button_text_3, callback_data=f"value,_count,{product_num},{count}"),
                            InlineKeyboardButton(text=button_text_4, callback_data=f"incr,_count,{product_num},{count}")
                            ],
                        [
                            InlineKeyboardButton(text=button_text_6, callback_data=f"finish,{product_num},{count}")
                            ],
                        [
                            InlineKeyboardButton(text=button_text_7, callback_data=f"finish"),
                            InlineKeyboardButton(text=button_text_8, callback_data=callback_text_8)
                            ]
                                        ],
                    resize_keyboard=True)

        # markup.insert(InlineKeyboardButton(text="-", callback_data=f"decr,count,{product_num},{count}"))
        # markup.insert(InlineKeyboardButton(text=f"{count}", callback_data=f"value,count,{product_num},{count}"))
        # markup.insert(InlineKeyboardButton(text="+", callback_data=f"incr,count,{product_num},{count}"))
        # markup.insert(InlineKeyboardButton(text="➕ 🛒", callback_data=f"finish,{product_num},{count}"))
        # markup.insert(InlineKeyboardButton(text=button_text_1, callback_data=callback_text_1))
        return markup



# async def product_info_btn(product_num: int, language=None):
#     logging.info("products info btn")
#     from loader import db 

#     # DB dan products objectini olish
#     try:
#         product_obj = await db.select_one_product(product_num)
#     except Exception as e:
#         logging.info(e)
#         product_obj = None

#     markup = InlineKeyboardMarkup(row_width=3)
#     if product_obj:
#         # Получаем клавиатуру с количеством продукта
#         product_num_kb = get_product_num(product_num)
        
#         # Кнопка назад
#         button_text_1 = "↩️ Ortga"
#         callback_text_1 = "_back_1"

#         if language == "ru":
#             button_text_1 = "↩️ Назад"
        
#         markup.add(*product_num_kb.inline_keyboard[0])  # Добавляем кнопки количества
#         markup.add(*product_num_kb.inline_keyboard[1])  # Добавляем кнопки количества
#         markup.insert(InlineKeyboardButton(text=button_text_1, callback_data=callback_text_1))
#     return markup



# Basket info btns
async def basket_info_btn(user_id: int, language=None):
    logging.info("basket info btn")
    from loader import db 

    # DB dan products objectini olish
    try:
        product_obj = await db.select_product_in_basket(user_id)
    except Exception as e:
        logging.info(e)
        product_obj = None

    # markup = InlineKeyboardMarkup(row_width=1)
    if product_obj:
        btn_text = "✅ Buyurtma berish"
        btn_text_1 = "❌ Bekor qilish"
        btn_text_2 = "↩️ Ortga"

        callback_text = f"product_basket"
        callback_text_1 = "cancel"
        callback_text_2 = "_back_1"

        if language == "ru":
            btn_text = "✅ Заказать"
            btn_text_1 = "❌ Отмена"
            btn_text_2 = "↩️ Назад"

        
        markup = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text=btn_text, callback_data=callback_text)],
                                [
                                    InlineKeyboardButton(text=btn_text_1, callback_data=callback_text_1),
                                    InlineKeyboardButton(text=btn_text_2, callback_data=callback_text_2)]
                                                ],
                            resize_keyboard=True)
        return markup

# bact from Basket btns
async def back_from_basket_btn(language=None):
    logging.info("back from basket btn")
    btn_text_1 = "↩️ Ortga"
    callback_text_1 = "_back_1"

    if language == "ru":
        btn_text_1 = "↩️ Назад"

    markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=btn_text_1, callback_data=callback_text_1)]
                                            ],
                        resize_keyboard=True)
    return markup


