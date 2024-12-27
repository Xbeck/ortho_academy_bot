import os


flag = "l"

if flag == "server":
    BOT_TOKEN = str(os.environ.get("BOT_TOKEN") )
    ADMINS = str(os.environ.get("ADMINS"))
    IP = str(os.environ.get("ip"))

    # # test token
    # # PROVIDER_TOKEN = str(os.environ.get("PROVIDER_TOKEN"))
    PROVIDER_TOKEN_PAYME = str(os.environ.get("PROVIDER_TOKEN_PAYME"))
    PROVIDER_TOKEN_CLICK = str(os.environ.get("PROVIDER_TOKEN_CLICK"))

    DB_USER = str(os.environ.get("DB_USER"))
    DB_PASS = str(os.environ.get("DB_PASS"))
    DB_NAME = str(os.environ.get("DB_NAME"))
    DB_HOST = str(os.environ.get("DB_HOST"))
    BOT_NICKNAME = str(os.environ.get("BOT_NICKNAME"))
    CHANNELS = str(os.environ.get("CHANNELS"))

else:
    from environs import Env
    #  for local PC
    # environs kutubxonasidan foydalanish
    env = Env()
    env.read_env()

    # .env fayl ichidan quyidagilarni o'qiymiz
    BOT_TOKEN = env.str("BOT_TOKEN_LOCAL")
    ADMINS = env.list("ADMINS_LOCAL")
    IP = env.str("ip")

    PROVIDER_TOKEN_PAYME = env.str("PROVIDER_TOKEN_PAYME_TEST")
    PROVIDER_TOKEN_CLICK = env.str("PROVIDER_TOKEN_CLICK_TEST")
    # PROVIDER_TOKEN_TRANZZO_TEST = env.str("PROVIDER_TOKEN_TRANZZO_TEST")


    DB_USER = env.str("DB_USER")
    DB_PASS = env.str("DB_PASS")
    DB_NAME = env.str("DB_NAME")
    DB_HOST = env.str("DB_HOST")
    BOT_NICKNAME = env.str("BOT_NICKNAME_LOCAL")
    CHANNELS = env.str("CHANNELS_LOCAL")


COMMANDS_LIST = [
                    "📎 Akount linki", "📎 Ссылка на аккаунт",
                    "🇺🇿 Til", "🇷🇺 Язык",
                    "👤 Obunachilar", "👤 Подписчики",
                    "💭 E'lon yo'llash", "💭 Объявление",
                    "📨 Doktorga savol", "📨 Обращение к Доктору",
                    "↩️ Назад", "↩️ Ortga",
                    "❕ помощь", "❕ help",

                    "/start", "/business_account", "/help"]

