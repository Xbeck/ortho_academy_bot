from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




# xizmat turlarini chiqaradi
async def show_servis_type_btn(service_list, language):

    # servis listni o'zgaradigan qilish kerak
    # list = ['Konsultatsiya', 'Terapiya']

    markup = InlineKeyboardMarkup(row_width=1)
    # logging.info(len(service_list))

    for i in range(0, len(service_list)//3):
        # logging.info(i)  # Terapiya-Терапия-1soat

        button_text = service_list[i]
        # logging.info(button_text)

        working_time = service_list[i+2]
        # logging.info(working_time)

        if language == 'ru':
            button_text = service_list[i+1]
            # logging.info(button_text)

        callback_data = f"{button_text.lower()},{working_time},serv"
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    return markup