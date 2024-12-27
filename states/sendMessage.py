from aiogram.dispatcher.filters.state import StatesGroup, State


#? -------------------------- Docga message yuborish states ---------------------
class FromUserToDoc(StatesGroup):
  # 1 ta holatdan o'tishi kerak
  message_text = State()
  finish = State()


class FromDocToUser(StatesGroup):
  # 1 ta holatdan o'tishi kerak
  message_text = State()
  finish = State()