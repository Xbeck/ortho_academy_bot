import logging
import re
from typing import Union
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import types

# -------------- local moduls ----------------
from keyboards.inline.markets_keyboards import back_from_basket_btn, basket_info_btn, product_info_btn
from loader import dp, db
from functions.all_functions import (
                                    get_user_data,
                                    message_fillter)









# # Markets Products list
# @dp.message_handler(text_contains="🛍")
# async def show_products_list(message: Message):
#     logging.info("Markets, Products list")
#     logging.info(message)
#     language, user_obj, tel_id = await get_user_data(message)
#     msg_ru = "Продукты"
#     msg_uz = "Mahsulotlar"
#     msg = await message_fillter(language, msg_ru, msg_uz)
#     await message.answer(msg, reply_markup=ReplyKeyboardRemove())
#     # inline menu
#     await message.delete()
#     msg_ru = "Выберите продукт"
#     msg_uz = "Mahsulot tanlang"
#     msg = await message_fillter(language, msg_ru, msg_uz)
#     await message.answer(msg, reply_markup=await products_menu_btn(language))


# # Products info
# @dp.callback_query_handler(text_contains="products_info")
# async def show_product_info(call: CallbackQuery):
#     logging.info("Products info")
#     logging.info(call.data)
#     language, user_obj, tel_id = await get_user_data(call)

#     product_num = int(call.data.split(",")[-1])
#     # DB dan products objectini olish
#     try:
#         product_obj = await db.select_one_product(product_num)
#     except Exception as e:
#         logging.info(e)
#         product_obj = None

#     product_photo_id = product_obj["photo_id"]
#     product_name = product_obj["name"]
#     product_discription = product_obj["discription"]
#     product_price = product_obj["price"]

#     msg_ru = ""
#     msg_uz = ""
#     if product_name:
#         msg_uz += f"\n{product_name}"
#         if language == "ru":
#             msg_ru += f"\n{product_name}"
#     if product_discription:
#         msg_uz += f"\n{product_discription}"
#         if language == "ru":
#             msg_ru += f"\n{product_discription}"
#     if product_price:
#         msg_uz += f"\n\n{product_price}"
#         if language == "ru":
#             msg_ru += f"\n\n{product_price}"

#     if product_photo_id:
#         if re.findall(r"\|", product_photo_id):
#             photo_id_list = product_photo_id.split("|")
#             album = types.MediaGroup()
#             for photo_id in photo_id_list:
#                 album.attach_photo(photo=photo_id)
#                 # album.attach_video(video=video1, caption="XPang Elekto Carning rasm va videolari")
#             await call.message.delete()
#             msg = await message_fillter(language, msg_ru, msg_uz)
#             await call.message.answer_media_group(media=album)
#             await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
#             await call.answer()
#         else:
#             await call.message.delete()
#             msg = await message_fillter(language, msg_ru, msg_uz)
#             await call.message.answer_photo(photo=product_photo_id, caption=msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
#             # await call.message.answer_photo()
#             await call.answer()
#     else:
#         msg = await message_fillter(language, msg_ru, msg_uz)
#         await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
#         await call.answer()



@dp.message_handler(text_contains="🛍 Market")
async def show_menu_product_default(message: types.Message):
    language, user_obj, tel_id = await get_user_data(message)
    await message.answer(text="Tavarlar", reply_markup=ReplyKeyboardRemove())
    await generate_product_info(language, product_num=1, message=message)

@dp.callback_query_handler(text_contains="🛍 Market")
async def show_menu_product_inline(call: types.CallbackQuery):
    language, user_obj, tel_id = await get_user_data(call)
    await call.message.answer(text="Tavarlar", reply_markup=ReplyKeyboardRemove())
    await generate_product_info(language, product_num=1, call=call)

    # await call.message.e




# async def menu_categories(message: Union[CallbackQuery, Message], **kwargs):
# generate product info:
async def generate_product_info(language, product_num=1, call=None, message=None):
    logging.info("Products info")
    # DB dan products objectini olish
    try:
        product_obj = await db.select_one_product(id=product_num)
        logging.info(product_obj)
    except Exception as e:
        logging.info(e)
        product_obj = None

    msg_ru = ""
    msg_uz = ""
    if product_obj:
        product_photo_id = product_obj["photo_id"]
        product_name = product_obj["name"]
        product_discription = product_obj["discription"]
        product_price = product_obj["price"]
    else:
        product_photo_id = None
        product_name = None
        product_discription = None
        product_price = None
        msg_ru = "Информация не найдена"
        msg_uz = "Malumot topilmadi"

    if product_name:
        msg_uz += f"\n{product_name}"
        if language == "ru":
            msg_ru += f"\n{product_name}"
    if product_discription:
        msg_uz += f"\n{product_discription}"
        if language == "ru":
            msg_ru += f"\n{product_discription}"
    if product_price:
        msg_uz += f"\n\nNarxi: {product_price}"
        if language == "ru":
            msg_ru += f"\n\nСтоимость: {product_price}"

    if product_photo_id:
        if re.findall(r"\|", product_photo_id):
            album = types.MediaGroup()
            photo_id_list = str(product_photo_id).split("|")

            logging.info(photo_id_list)
            # for i, photo_id in enumerate(photo_id_list):
            #     logging.info(photo_id)
            #     if photo_id:  # Проверяем, что photo_id не None и не пустая строка
            #         album.attach_photo(photo=photo_id)

                # album.attach_video(video=video1, caption="XPang Elekto Carning rasm va videolari")
            msg = await message_fillter(language, msg_ru, msg_uz)
            if call:
                await call.message.delete()
                # await call.message.answer_media_group(media=album)
                await call.message.answer_photo(photo=photo_id_list[0])
                # await call.message.edit_text(msg)
                # await call.message.edit_reply_markup(reply_markup=await product_info_btn(product_num=product_num, language=language))
                await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
                await call.answer()
            else:
                await message.delete()
                # await message.answer_media_group(media=album)
                await message.answer_photo(photo=photo_id_list[0])
                # await message.edit_text(msg)
                # await message.edit_reply_markup(reply_markup=await product_info_btn(product_num=product_num, language=language))
                await message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
        else:
            msg = await message_fillter(language, msg_ru, msg_uz)
            if call:
                await call.message.delete()
                await call.message.answer_photo(photo=product_photo_id, caption=msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
                # await call.message.answer_photo()
                await call.answer()
            else:
                await message.delete()
                await message.answer_photo(photo=product_photo_id, caption=msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
                # await message.answer_photo()
                await call.answer()
    else:
        msg = await message_fillter(language, msg_ru, msg_uz)
        if call:
            await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
            await call.answer()
        else:
            await message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))






# # Products info first in
# @dp.message_handler(text_contains="🛍")
# async def show_products_list(message: Message):
#     logging.info("Products info")
#     logging.info(message)
#     language, user_obj, tel_id = await get_user_data(message)

#     msg_ru = "Продукты"
#     msg_uz = "Mahsulotlar"
#     msg = await message_fillter(language, msg_ru, msg_uz)
#     await message.answer(msg, reply_markup=ReplyKeyboardRemove())

#     product_num = 1
#     # DB dan products objectini olish
#     try:
#         product_obj = await db.select_one_product(id=1)
#     except Exception as e:
#         logging.info(e)
#         product_obj = None

#     product_photo_id = product_obj["photo_id"]
#     product_name = product_obj["name"]
#     product_discription = product_obj["discription"]
#     product_price = product_obj["price"]

#     msg_ru = ""
#     msg_uz = ""
#     if product_name:
#         msg_uz += f"\n{product_name}"
#         if language == "ru":
#             msg_ru += f"\n{product_name}"
#     if product_discription:
#         msg_uz += f"\n{product_discription}"
#         if language == "ru":
#             msg_ru += f"\n{product_discription}"
#     if product_price:
#         msg_uz += f"\n\nNarxi: {product_price}"
#         if language == "ru":
#             msg_ru += f"\n\nСтоимость: {product_price}"

#     if product_photo_id:
#         if re.findall(r"\|", product_photo_id):
#             photo_id_list = product_photo_id.split("|")
#             album = types.MediaGroup()
#             logging.info(photo_id_list)
#             for photo_id in photo_id_list:
#                 if photo_id is not None and album is not None:
#                     album.attach_photo(photo=photo_id)
#                 else:
#                     # Обработка ошибки или вывод сообщения о проблеме
#                     print("photo_id или album имеют значение None")
#                 # album.attach_video(video=video1, caption="XPang Elekto Carning rasm va videolari")
#             await message.delete()
#             msg = await message_fillter(language, msg_ru, msg_uz)
#             await message.answer_media_group(media=album)
#             await message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
#         else:
#             await message.delete()
#             msg = await message_fillter(language, msg_ru, msg_uz)
#             await message.answer_photo(photo=product_photo_id, caption=msg, reply_markup=await product_info_btn(product_num=product_num, language=language))

#     else:
#         msg = await message_fillter(language, msg_ru, msg_uz)
#         await message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))






# Next Products info >>
@dp.callback_query_handler(text_contains="_next") # _previous
async def show_next_product_info(call: CallbackQuery):
    logging.info("Next Products info >>")
    logging.info(call.data)
    language, user_obj, tel_id = await get_user_data(call)

    # DB dan products objectini olish
    product_count = await db.count_product()
    triger, product_num, count = call.data.split(",")
    if product_count <= int(product_num):
        product_num = 1
    else:
        product_num = int(product_num) + 1
    await generate_product_info(language=language, call=call, product_num=product_num)


# Next Products info >>
@dp.callback_query_handler(text_contains="_previous")
async def show_previous_product_info(call: CallbackQuery):
    logging.info("Previous Products info <<")
    logging.info(call.data)
    language, user_obj, tel_id = await get_user_data(call)

    # DB dan productlar sonini olish
    product_count = await db.count_product()

    triger, product_num, count = call.data.split(",")

    if int(product_num) == 1:
        product_num = product_count
    else:
        product_num = int(product_num) - 1
    await generate_product_info(language=language, call=call, product_num=product_num)

    # # DB dan products objectini olish
    # try:
    #     product_obj = await db.select_one_product(id=1)
    # except Exception as e:
    #     logging.info(e)
    #     product_obj = None

    # product_photo_id = product_obj["photo_id"]
    # product_name = product_obj["name"]
    # product_discription = product_obj["discription"]
    # product_price = product_obj["price"]

    # msg_ru = ""
    # msg_uz = ""
    # if product_name:
    #     msg_uz += f"\n{product_name}"
    #     if language == "ru":
    #         msg_ru += f"\n{product_name}"
    # if product_discription:
    #     msg_uz += f"\n{product_discription}"
    #     if language == "ru":
    #         msg_ru += f"\n{product_discription}"
    # if product_price:
    #     msg_uz += f"\n\nNarxi: {product_price}"
    #     if language == "ru":
    #         msg_ru += f"\n\nСтоимость: {product_price}"

    # if product_photo_id:
    #     if re.findall(r"\|", product_photo_id):
    #         photo_id_list = product_photo_id.split("|")
    #         album = types.MediaGroup()
    #         for photo_id in photo_id_list:
    #             album.attach_photo(photo=photo_id)
    #             # album.attach_video(video=video1, caption="XPang Elekto Carning rasm va videolari")
    #         await call.message.delete()
    #         msg = await message_fillter(language, msg_ru, msg_uz)
    #         await call.message.answer_media_group(media=album)
    #         await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
    #         await call.answer()
    #     else:
    #         await call.message.delete()
    #         msg = await message_fillter(language, msg_ru, msg_uz)
    #         await call.message.answer_photo(photo=product_photo_id, caption=msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
    #         # await call.message.answer_photo()
    #         await call.answer()
    # else:
    #     msg = await message_fillter(language, msg_ru, msg_uz)
    #     await call.message.answer(msg, reply_markup=await product_info_btn(product_num=product_num, language=language))
    #     await call.answer()




@dp.callback_query_handler(text_contains="_count")
async def callback_num_change(call: CallbackQuery):
    logging.info("count")
    language, user_obj, tel_id = await get_user_data(call)
    logging.info(call.data)

    # Получаем новый номер продукта из callback_data
    call_data, triger, product_num, count = call.data.split(',')
    product_count = int(count)

    # Получаем новое значение для кнопки
    # Изменяем значение в зависимости от действия
    if call_data == "decr":
        product_count = product_count - 1
        if product_count > 0:
            # Редактируем сообщение с обновленной клавиатурой
            await call.message.edit_reply_markup(reply_markup=await product_info_btn(product_num=int(product_num),
                                                                                    language=language,
                                                                                    callback=int(product_count)))
    elif call_data == "incr" and product_count >= 1:
        product_count += 1
        # Редактируем сообщение с обновленной клавиатурой
        await call.message.edit_reply_markup(reply_markup=await product_info_btn(product_num=int(product_num),
                                                                                language=language,
                                                                                callback=int(product_count)))
    else:
        pass
    await call.answer()


# Products in Basket
@dp.callback_query_handler(text_contains="finish")
async def add_product_basket_show(call: CallbackQuery):
    logging.info("Product to basket | Show basket | finish")
    logging.info(call.data)
    language, user_obj, tel_id = await get_user_data(call)


    # DB dan products objectini olish
    try:
        basket_objs = await db.select_product_in_basket(user_obj["id"])
        logging.info(basket_objs)
    except Exception as e:
        logging.info(e)
        basket_objs = None

    if re.findall(r"\,", call.data):
        triger, product_num, count = call.data.split(",")
        if product_num in basket_objs:
            logging.info("update basket")
            await db.update_basket_product(product_id=int(product_num), count=count, user_id=user_obj["id"])
        else:
            logging.info("add to basket")
            # DB basket ga product id ni qo'shish
            await db.add_to_basket(product_id=int(product_num), user_id=int(user_obj["id"]), count=int(count))
    else:
        logging.info("go to basket")

    basket_objs = await db.select_product_in_basket(user_obj["id"])
    msg_ru = "Корзина:"
    msg_uz = "Savat:"
    if basket_objs:
        price_value = 0
        for i, basket in enumerate(basket_objs):
            logging.info(basket)
            product_id = basket["product_id"]
            product = await db.select_one_product(id=product_id)
            logging.info(product)
            product_name = product["name"]

            count = basket["count"]
            price = product['price']
            price_value += int(price) * count

            msg_uz += f"\n{product_name} --- {count}"
            if language == "ru":
                msg_ru += f"\n{product_name} --- {count}"

        msg_uz += f"\n------------------- ------------------- \n\n--------- {price_value} so'm---------"
        if language == "ru":
            msg_ru += f"\n------------------- ------------------- \n\n--------- {price_value} сум ---------"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await call.message.delete()
        await call.message.answer(msg, reply_markup=await basket_info_btn(user_id=user_obj["id"], language=language))
    else:
        msg_uz += f"\n\nTavar savatga qo'shilmagan"
        if language == "ru":
            msg_ru += f"\n\nТовар не добавлен в корзину"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await call.message.delete()
        await call.message.answer(msg, reply_markup=await back_from_basket_btn(language=language))

    await call.answer()


# Cancel order in Basket
@dp.callback_query_handler(text_contains="cancel")
async def add_product_basket_show(call: CallbackQuery):
    logging.info("cancel all product")
    logging.info(call.data)
    language, user_obj, tel_id = await get_user_data(call)

    # DB basket ichidagi product larni o'chirish
    await db.delete_product_from_basket(user_id=user_obj["id"])
    await add_product_basket_show(call=None)
    await call.answer()


