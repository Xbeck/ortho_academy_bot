from aiogram.dispatcher.filters.state import StatesGroup, State


#? -------------------------- Userlarga reklama yuborish states ---------------------
class ReklamaData(StatesGroup):
  # 1 ta holatdan o'tishi kerak
  text_reklama = State()
  finish = State()