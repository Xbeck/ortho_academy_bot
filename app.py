from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands




async def on_startup(dispatcher):
    # db bilan aloqa o'rnatamiz:
    await db.create()
    # users jadvalni o'chirish:
    # await db.drop_courses()
    # await db.drop_shoppings()
    # await db.drop_baskets()
    # await db.drop_products()
    # await db.drop_users()

    # users jadvalini yaratamiz:
    await db.create_table_users()
    await db.create_table_products()
    await db.create_table_baskets()
    await db.create_table_shoppings()
    await db.create_table_courses()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

# """
# Assalom alaykum!
# Botimiz sizga tez va qulay xizmat ko'rsatish uchun yaratilgan
# bo'lib, o'zingizni qiziqtirgan muhim savollaringizga javob berish
# bilan shug'ullanadi.

# Привет!
# Наш бот создан для быстрого и удобного обслуживания и
# занимается ответами на ваши важные вопросы."""