from aiogram import types

# from data.config import ADMINS




async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish | "),
            # types.BotCommand("user_account", "Klientlar interface-ini ko'rish"),
            # types.BotCommand("stop", "Ma'lumot kiritish jarayonini to'xtatadi"),
            # types.BotCommand("book", "Kitob haqida ma'lumot"),
            # types.BotCommand("praktikum", "Kurs haqida ma'lumot"),
            # types.BotCommand("mahsulotlar", "Kurslar"),
            types.BotCommand("help", "Yordam"),
        ]
    )