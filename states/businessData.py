from aiogram.dispatcher.filters.state import StatesGroup, State




# biznes account ochish states  
class CreateBusinessAccount(StatesGroup):
    # 3 ta holatdan o'tishi kerak
    profession = State()
    biography = State()
    photo_id = State()
    finish = State()



# biznes accountni ish vaqti
class InsertWorkTime(StatesGroup):
    start_end_time = State()
    finish = State()


# biznes accountni xizmat turlari 
class ServiceTypeAndTime(StatesGroup):
    service_and_time = State()
    finish = State()


class AccountChangePhoto(StatesGroup):
    photo = State()
    finish = State()

# businis account setings state
# Account Photo
class EditAccountPhoto(StatesGroup):
    new_element = State()
    finish = State()
# Biograph
class EditAccountBiograph(StatesGroup):
    new_element = State()
    finish = State()
# GeoLocation
class EditAccountLocation(StatesGroup):
    new_element = State()
    finish = State()
# Url
class EditAccountUrl(StatesGroup):
    new_element = State()
    finish = State()
# Profession 
class EditAccountProfession(StatesGroup):
    new_element = State()
    finish = State()
# Address 
class EditAccountAddress(StatesGroup):
    new_element = State()
    finish = State()



# Question append
class AppendTemplateQuestion(StatesGroup):
    get_element = State()
    finish = State()

# Question edit
class EditTemplateQuestion(StatesGroup):
    get_element = State()
    finish = State()


