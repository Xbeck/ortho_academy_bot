import logging
from aiogram import types
from typing import Union
import re




async def admin_filter(flag: str, admin_list: list):
    ADMINS_LIST = admin_list
    if flag=="server":
        ADMINS_LIST = str(admin_list).split(",")
        return ADMINS_LIST
    return ADMINS_LIST


# user tili, user_obj va tel_id sini oladi
async def get_user_data(message: Union[types.Message, types.CallbackQuery]):
    from loader import db
    tel_id = message.from_user.id
    language = "uz"

    try:
        user_obj = await db.select_user(telegram_id=tel_id)
        language = user_obj["language"]
    except Exception as e:
        logging.info(e)

    return language, user_obj, tel_id



# busenes akount obj ni qaytaradi
async def get_busines_object(user_id: int) -> object:
    from loader import db
    logging.info("get busines obj")
    try:
        busines_obj = await db.select_businesses(user_id)
        logging.info(f"result: {busines_obj}")
    except Exception as e:
        logging.info(e)
        busines_obj = None
    return busines_obj



async def get_question_obj(user_obj: object) -> object:
    from loader import db

    busenes_obj = await get_busines_object(user_obj['id'])
    if busenes_obj:
        # Db dan User uchun o'z tel_id sini olish | oz accountini seting qilish uchun
        tel_id = str(user_obj['telegram_id'])
        # pass
    else:
        # Db dan User uchun referral_id ni olish | userga Docni saxifasini ko'rsatish uchun
        tel_id = str(user_obj['referral_id'])
    
    try:
        busenes_user_obj = await db.select_user(int(tel_id))
    except Exception as e:
        logging.info(e)
        busenes_user_obj = None

    # DB dan question objectni olish
    try:
        questions_obj = await db.select_questions(busenes_user_obj['id'])
    except Exception as e:
        logging.info(e)
        questions_obj = None
    return questions_obj


async def message_fillter(language, msg_ru=None, msg_uz=None):
    msg = msg_uz
    if language == "ru":
        msg = msg_ru
        return msg
    return msg


# takrorlanuvchi savollar un sarlavha
async def question_title(language: str) -> str:
    msg1 = await message_fillter(language,
                            "Часто задаваемые вопросы: \n",
                            "Ko'p beriladigan savollar: \n")
    msg2 = await message_fillter(language,
                            "------------------- ------------------- \n",
                            "------------------- ------------------- \n")
    return msg1, msg2


# business account uchun referral tel_id list
async def get_referral_list(user: object, tel_id: int):
    from loader import db
    business_account_obj_list = await db.select_all_business_accounts()

    for business_obj in business_account_obj_list:
        if business_obj[user['id']] is None:
            return business_obj
        
        referral_tel_id_list = await db.select_all_referral_id(referral_id=str(tel_id))
        return business_obj, referral_tel_id_list


# tekst dagi | symbol orqali uni ikkiga bo'ladi
async def split_text(language, text):
    if re.findall(r"\|", text):
        # 'Символ "|" присутствует в тексте'
        parts = text.split("|")
        result = parts[1] if language == "ru" else parts[0]
    else:
        # 'Символ "|" отсутствует в тексте'
        result = text
    return result.strip()


async def get_business_calendar(referral_id):
    from loader import db
    # DB dan DOC calendar id (email)ni oladi
    businis_account_tel_id = int(referral_id)
    businiss_accoun_obj = await db.select_user(businis_account_tel_id)
    calendar_obj = await db.select_calendar(user_id=businiss_accoun_obj['id'])
    calendar_id = calendar_obj['calendar_id']
    logging.info(calendar_id)
    return calendar_id

