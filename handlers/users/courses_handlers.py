import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import LabeledPrice



from data.config import ADMINS
from functions.all_functions import get_user_data, message_fillter
from keyboards.inline.doc_admin_keyboards import get_element_in_object
from loader import dp, bot, db
from data.products import course_invoise, orto_book, FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.inline.course_keyboards import build_keyboard
from utils.misc.product import Product








# @dp.message_handler(Command("mahsulotlar"))
# async def book_invoice(message: Message):
#     await bot.send_invoice(chat_id=message.from_user.id, **orto_book.generate_invoice(), payload="123456")
#     await bot.send_invoice(chat_id=message.from_user.id, **course_invoise(course_num).generate_invoice(), payload="123457")


# @dp.message_handler(text_contains="📒 Kurslar")
# async def all_invoice(message: Message):
# #     await bot.send_invoice(chat_id=message.from_user.id, **orto_book.generate_invoice(), payload="123456")
# #     await bot.send_invoice(chat_id=message.from_user.id, **orto_oflinecourse.generate_invoice(), payload="123457")

#     # await show_book_invoices(message)
#     await show_course_invoices(message)





# @dp.message_handler(Command("book"))
# async def show_book_invoices(message: types.Message):
#     language, user_obj, tel_id = await get_user_data(message)
#     caption = "<b>Pythonda Dasturlash Asoslari</b> kitobi.\n\n"
#     caption += "Ushbu kitob bugungi kunda dasturlash asoslariga oid o’zbek tilidagi mukammal tuzilgan qo’llanmalardan biridir.\n\n"
#     caption += "Qo’lingizdagi kitobning o’ziga xos jihati shundaki, uning har bir bo’limi uchun tayyorlangan qo'shimcha onlayn"
#     caption += "materiallar, jumladan, 50 dan ortiq video darslar, amaliy mashg’ulotlar va vazifalarning kodlari e’tiboringizga havola etilgan.\n\n"
#     caption += "O’quvchilar bu materiallarni maxsus QR kod yordamida o’z komputerlariga yuklab olib, ulardan unumli foydalanishi mumkin.\n\n"
#     caption += "Narxi: <b>50000 so'm</b>"
#     await message.answer_photo(photo="https://i.imgur.com/0IvPPun.jpg",
#                                caption=caption,
#                                reply_markup=build_keyboard("book", language=language))


# @dp.callback_query_handler(text="product:book")
# async def book_invoice(call: CallbackQuery):
#     await bot.send_invoice(chat_id=call.from_user.id,
#                                                     **orto_book.generate_invoice(),
#                                                     payload="payload:kitob")
#     await call.answer()




@dp.message_handler(text_contains="📒 Kurslar")
async def show_course_invoices(message: types.Message):
    language, user_obj, tel_id = await get_user_data(message)

    try:
        courses_objs = await db.select_courses()
    except Exception as e:
        logging.info(e)
        courses_objs = None

    if courses_objs:
        for course in courses_objs:
            title = await get_element_in_object(obj=course, column_name='course_title')
            # photo_url = await get_element_in_object(obj=course, column_name='course_img_url')
            photo_url = None
            discription = await get_element_in_object(obj=course, column_name='course_discription')
            plane = await get_element_in_object(obj=course, column_name='course_plan')
            price = await get_element_in_object(obj=course, column_name='course_price')
            discount = await get_element_in_object(obj=course, column_name='course_discount')
            currency = await get_element_in_object(obj=course, column_name='currency')


            caption = f"<b>{title}</b>\n\n"
            caption += f"{discription}\n\n"

            if plane:
                plane_list = plane.split(".")
                caption += f"Kurs tarkibi:\n"
                for i, plan in enumerate(plane_list):
                    if i >= len(plane_list) - 1:
                        caption += f" \n\n"
                        break
                    else:
                        caption += f"✅ {plan}\n"
            if price:
                caption += f"Narxi: <b>{int(price) / 100} so'm</b>"
            else:
                caption += f"Narxi: <b> 0 so'm</b>"

            if photo_url:
                # logging.info(photo_url)
                await message.answer_photo(photo=photo_url,
                                    caption=caption,
                                    reply_markup=await build_keyboard(f"{course['id']}", language=language))
            else:
                await message.answer(text=caption,
                                    reply_markup=await build_keyboard(f"{course['id']}", language=language))
    else:
        msg_ru = "Курсы не найдены"
        msg_uz = "Kurslar topilmadi"
        msg = await message_fillter(language, msg_ru, msg_uz)
        await message.answer(msg)


    # caption = "<b>Data Science va Sun'iy Intellekt</b> praktikum.\n\n"
    # caption += "6 oyda eng zamonaviy kasb egasi bo'ling.\n\n"

    # caption += "Kurs tarkibi:\n"
    # caption += "✅ Python Dasturlash Asoslar (4 hafta)\n"
    # caption += "✅ Data Sciencega kirish va DS metodologiyasi (2 hafta)\n"
    # caption += "✅ Ma'lumotlar tahlili (Data Analysis) (4 hafta)\n"
    # caption += "✅ Ma'lumotlarga ishlov berish (4 hafta)\n"
    # caption += "✅ Vizualizasiya (2 hafta)\n"
    # caption += "✅ Machine Learning (6 hafta)\n"
    # caption += "✅ Deep Learning (4 hafta)\n"
    # caption += "✅ Natural Language Processing (4 hafta)\n\n"
    # caption += "Narxi: <b>1.5mln so'm</b>"
    # await message.answer_photo(photo="https://i.imgur.com/vRN7PBT.jpg",
    #                            caption=caption,
    #                            reply_markup=build_keyboard("praktikum", language=language))







@dp.callback_query_handler(text_contains="buy_course:")
async def praktikum_invoice(call: CallbackQuery):
    course_num = int(call.data.split(":")[-1])

    try:
        courses_obj = await db.select_one_course(id=int(course_num))
    except Exception as e:
        logging.info(e)
        courses_obj = None

    if courses_obj:
        chegirma = courses_obj['course_discount']
        if chegirma:
            course = Product(
                title = courses_obj['course_title'],
                description = courses_obj['course_discription'],
                currency = "UZS",
                prices = [
                    LabeledPrice(
                        label = "Praktikum",
                        amount = int(courses_obj['course_price']), #150.00$
                    ),
                    LabeledPrice(
                        label="Chegirma",
                        amount=-int(chegirma), #-10.00$
                    ),
                ],
                start_parameter = "create_invoice_ds_praktikum",
                photo_url = courses_obj['course_img_url'],
                photo_width=650,
                photo_height=280,
                need_name=True,
                need_phone_number=True)
        else:
            course = Product(
                title = courses_obj['course_title'],
                description = courses_obj['course_discription'],
                currency = "UZS",
                prices = [
                    LabeledPrice(
                        label = "Praktikum",
                        amount = int(courses_obj['course_price']), #150.00$
                        )
                ],
                start_parameter = "create_invoice_ds_praktikum",
                photo_url = courses_obj['course_img_url'],
                photo_width=650,
                photo_height=280,
                need_name=True,
                need_phone_number=True)
    # course = course_invoise(course_num)
    await call.message.delete()
    await bot.send_invoice(chat_id=call.from_user.id,
                                                    **course.generate_invoice(),
                                                    payload="payload:praktikum")
    await call.answer()






@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                                                        ok=False,
                                                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "tashkent":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    # klientga xabar yuborish, xarid xaqida:
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                            text="Xaridingiz uchun rahmat!")
    # adminga xabar yuborish, xarid xaqida:
    await bot.send_message(chat_id=ADMINS[0],
                            text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                    f"ID: {pre_checkout_query.id}\n"
                                    f"Telegram user: {pre_checkout_query.from_user.first_name}\n"                                
                                    f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")