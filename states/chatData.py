from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatBot(StatesGroup):
  # Foydalanuvchi buyerda 1 ta holatdan o'tishi kerak
  question = State()
  finish = State()


class AddQuestionToChatBot(StatesGroup):
  # Foydalanuvchi buyerda 2 ta holatdan o'tishi kerak
  question = State()
  answer = State()
  finish = State()