from aiogram import Dispatcher

from loader import dp
from middlewares.checksub import BigBrother
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())
