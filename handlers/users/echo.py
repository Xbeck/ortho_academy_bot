import logging
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS, BOT_TOKEN
from functions.all_functions import get_user_data, message_fillter
from loader import dp, bot



# # photo jo'natish:
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_file_id_p(message: types.Message):
    language, user, tel_id = await get_user_data(message)
    photo_id = message.photo[-1].file_id
    if str(tel_id) in ADMINS:
        await message.reply(photo_id)
        # await message.answer(photo_id)
        #   await message.answer_photo(photo=photo_id)

        # Получаем объект файла с помощью file_id
        file = await bot.get_file(photo_id)
        file_path = file.file_path
        await message.answer(file_path)

        # Формируем URL для загрузки файла
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        await message.answer(file_url)


# video jo'natish:
@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_file_id_v(message: types.Message):
    language, user, tel_id = await get_user_data(message)
    video_id = message.video.file_id
    if str(tel_id) in ADMINS: 
        await message.reply(video_id)


# animatsiya(gif) jo'natish:
@dp.message_handler(content_types=types.ContentType.ANIMATION)
async def get_file_id_a(message: types.Message):
    language, user, tel_id = await get_user_data(message)
    if str(tel_id) in ADMINS:
        await message.reply(message.animation.file_id)


# Echo chat bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    logging.info('echo')
    language, user, tel_id = await get_user_data(message)

    if str(tel_id) in ADMINS:
        result = await bot.get_chat(chat_id="@ortho_academy")
        await message.reply(result)
    else:
        msg = await message_fillter(language,
                            "Подобная информация не найдена!",
                            "Bunday ma'lumot topilmadi!")
        await message.answer(msg)


# Обработчик команды /stop для выхода из состояния
# @dp.message_handler(commands=['stop'], state='*')
# async def cmd_stop(message: types.Message, state: FSMContext):
#     language, user, tel_id = await get_user_data(message)
#     msg_ru = f"Вы вышли из всех состояний."
#     msg_uz = f"Siz hamma state-lardan chiqdingiz."
#     msg = await message_fillter(language, msg_ru, msg_uz)

#     await state.finish()
#     await message.reply(msg)
