from aiogram.dispatcher.filters.state import StatesGroup, State


#? -------------------------- Shaxsiy ma'lumotlarni yig'sih uchun PersonalData holatdan yaratamiz ---------------------
class PersonalData(StatesGroup):
    # Foydalanuvchi buyerda  ta holatdan o'tishi kerak
    full_name = State()
    # name = State()
    # birthday = State()
    phone = State()
    finish = State()


class GetCourseTitle(StatesGroup):
    title = State()
    finish = State()
class GetCourseDiscription(StatesGroup):
    discription = State()
    finish = State()
class GetCourseImgUrl(StatesGroup):
    img_url = State()
    finish = State()
class GetCoursePlan(StatesGroup):
    plan = State()
    finish = State()
class GetCoursePrice(StatesGroup):
    price = State()
    finish = State()
class GetCourseDiscount(StatesGroup):
    discount = State()
    finish = State()