from cProfile import label
import logging
from xmlrpc.client import TRANSPORT_ERROR
from aiogram import types
from aiogram.types import LabeledPrice

from utils.misc.product import Product




pro_podpiska = Product(
    title="💠 Pro Podpiska",
    description="Pro Funksional ichiga Telegraph statiya generatsiya",
    currency="UZS",
    prices=[
        LabeledPrice(
            label="1 oy",
            amount=50000, #5.00$
        ),
        LabeledPrice(
            label="10 oy",
            amount=500000, #5.00$
        ),
    ],
    start_parameter="create_invoice_pro_podpiska",
    need_name=True,
    need_phone_number=True
    )



async def course_invoise(course_num: int):
    from loader import db
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
        return course
    return None






orto_book = Product(
    title="Pythonda Dasturlash asoslari",
    description="Kitobga to'lov qilish uchun quyidagi tugmani bosing.",
    currency="UZS",
    prices=[
        LabeledPrice(
            label="Kitob",
            amount=500000, #5.00$
        ),
        LabeledPrice(
            label="Yetkazib berish (7 kun)",
            amount=10000, #1.00$
        ),
    ],
    start_parameter="create_invoice_python_book",
    photo_url='https://i.imgur.com/0IvPPun.jpg',
    photo_width=650,
    photo_height=280,
    # photo_size=800,
    need_name=True,
    need_phone_number=True,
    # need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
    # is_flexible=True
    )





REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Fargo (3 kun)',
    prices=[
        LabeledPrice(
            'Maxsus quti', 100),
        LabeledPrice(
            '3 ish kunida yetkazish', 100),
    ]
    )

FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Express pochta (1 kun)',
    prices=[
        LabeledPrice(
            '1 kunda yetkazish', 100),
    ]
    )


PICKUP_SHIPPING = types.ShippingOption(
    id='pIckup',
    title="Do'kondan olib ketish",
    prices=[
        LabeledPrice(
            'Yetkazib berishsiz', -100),
    ]
    )