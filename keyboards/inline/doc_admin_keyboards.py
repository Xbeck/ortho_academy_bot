import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




async def cource_info_menu():
    from loader import db
    # course = await db.select_one_course(course_num)

    course_obj = await db.select_courses()
    curse_id_list = []
    for i in course_obj:
        curse_id_list.append(i['id'])
    course_num = sorted(curse_id_list)[-1] + 1

    course_obj = await db.select_courses()
    
    markup = InlineKeyboardMarkup(row_width=1)
    if course_obj:
        for course in course_obj:
            try:
                title = course["course_title"]
            except Exception as e:
                logging.info(e)
                title = None
            
            if title:
                btn_text = course["course_title"]
            else:
                btn_text = course["id"]
            callback_text = f'_edit_course:{course["id"]}'
            markup.insert(InlineKeyboardButton(text=btn_text, callback_data=callback_text))
    
    btn_text_2 = "➕ Kurs qo'shish"
    btn_text_3 = "↩️ ortga"
    callback_text_2 = f'_add_course:{course_num}'
    callback_text_3 = f'_back_0'
    markup.insert(InlineKeyboardButton(text=btn_text_2, callback_data=callback_text_2))
    markup.insert(InlineKeyboardButton(text=btn_text_3, callback_data=callback_text_3))
    return markup






async def get_element_in_object(obj: object, column_name: str):
    try:
        value = obj[f'{column_name}']
    except Exception as e:
        logging.info(e)
        value = None
    return value


async def cource_data_info_btn(course_num: int):
    from loader import db
    course = await db.select_one_course(course_num)

    btn_text_1 = "➕ Kurs sarlavhasi"
    btn_text_2 = "➕ Kurs haqida"
    btn_text_3 = "➕ Kurs image"
    btn_text_4 = "➕ Kurs tarkibi | rejasi"
    btn_text_5 = "➕ Kurs narxi"
    btn_text_6 = "➕ Kursga chegirma"
    btn_text_7 = "↩️ ortga"

    title = await get_element_in_object(course, "course_title")
    discription = await get_element_in_object(course, "course_discription")
    img_url = await get_element_in_object(course, "course_img_url")
    plan = await get_element_in_object(course, "course_plan")
    price = await get_element_in_object(course, "course_price")
    discount = await get_element_in_object(course, "course_discount")

    callback_1 = f"_title:{course_num}"
    callback_2 = f"_discription:{course_num}"
    callback_3 = f"_img_url:{course_num}"
    callback_4 = f"_plan:{course_num}"
    callback_5 = f"_price:{course_num}"
    callback_6 = f"_discount:{course_num}"

    
    if title:
        btn_text_1 = "✏️ Sarlavhani tahrirlash"
        # callback_1 = f"_title:edit:{course_num}"
    if discription:
        btn_text_2 = "✏️ Kurs info sini tahrirlash"
        # callback_2 = f"_discription:edit:{course_num}"
    if img_url:
        btn_text_3 = "✏️ Rasmini o'zgartirish"
        # callback_3 = f"_img_url:edit:{course_num}"
    if plan:
        btn_text_4 = "✏️ Kurs tarkibi | rejasini tahrirlash"
        # callback_4 = f"_plan:edit:{course_num}"
    if price:
        btn_text_5 = "✏️ Narxini tahrirlash"
        # callback_5 = f"_price:edit:{course_num}"
    if discount:
        btn_text_6 = "✏️ Chegirmani tahrirlash"
        # callback_6 = f"_discount:edit:{course_num}"
        

    callback_7 = f"_back_1"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text_1, callback_data=callback_1)],
        [InlineKeyboardButton(text=btn_text_2, callback_data=callback_2)],
        [InlineKeyboardButton(text=btn_text_3, callback_data=callback_3)],
        [InlineKeyboardButton(text=btn_text_4, callback_data=callback_4)],
        [InlineKeyboardButton(text=btn_text_5, callback_data=callback_5)],
        [InlineKeyboardButton(text=btn_text_6, callback_data=callback_6)],
        [InlineKeyboardButton(text=btn_text_7, callback_data=callback_7)]
    ])
    return markup