from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# local moduls
from functions.all_functions import message_fillter




async def phone_btn(language):
  btn_text = await message_fillter(language,
                             "Отправить номер телефона",
                             "Telefon raqamni yuborish")
  markup = ReplyKeyboardMarkup(
    keyboard=[[
                KeyboardButton(text=btn_text, request_contact=True)
              ]],
    resize_keyboard=True,
    one_time_keyboard=True)
  return markup