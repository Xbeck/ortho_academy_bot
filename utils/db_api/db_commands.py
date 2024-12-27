from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config




class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
                                                user=config.DB_USER,
                                                password=config.DB_PASS,
                                                host=config.DB_HOST,
                                                database=config.DB_NAME
                                                )

    async def execute(self, command, *args,
                        fetch: bool = False,
                        fetchval: bool = False,
                        fetchrow: bool = False,
                        execute: bool = False
                        ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # --------------------------- Users jadvali ---------------------------
    async def create_table_users(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(35) NULL,
                username varchar(35) NULL,
                telegram_id BIGINT NOT NULL UNIQUE,
                language VARCHAR(3) NULL,
                phone_number VARCHAR(13) NULL
                );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                            start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name=None, username=None, telegram_id=None, language=None, phone_number=None):
        sql = "INSERT INTO users (full_name, username, telegram_id, language, phone_number) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, language, phone_number, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def user_exists(self, telegram_id):
        sql = "SELECT EXISTS(SELECT 1 FROM Users WHERE telegram_id=$1)"
        return await self.execute(sql, telegram_id, fetchval=True)
    
    async def select_all_tel_id(self):
        sql = "SELECT telegram_id FROM Users"
        return await self.execute(sql, fetchval=True)
    
    async def count_referrals(self, referral_id):
        sql = "SELECT COUNT(*) FROM Users WHERE referral_id=$1"
        return await self.execute(sql, referral_id, fetchval=True)

    #   async def select_user(self, **kwargs):
    #     sql = "SELECT * FROM Users_ WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetchrow=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)
  
    async def select_user_tel_id(self, user_id):
        sql = "SELECT telegram_id FROM Users WHERE id=$1"
        return await self.execute(sql, user_id, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)


    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_referral_id(self, referral_id, telegram_id):
        sql = "UPDATE Users SET referral_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, referral_id, telegram_id, execute=True)
  
    async def update_user_all_data(self, telegram_id, full_name=None, username=None, language=None, phone_number=None):
        sql = "UPDATE Users SET full_name=$2, username=$3, language=$4, phone_number=$5 WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, full_name, username, language, phone_number, fetchrow=True)
  
    # update user data
    async def update_user_data(self, full_name_tel, phone_number, telegram_id): # full_name, birthday,
        sql = "UPDATE Users SET full_name_tel=$1, phone_number=$2 WHERE telegram_id=$3"
        return await self.execute(sql, full_name_tel, phone_number, telegram_id, execute=True)

    async def update_user_language(self, language, telegram_id):
        sql = f"UPDATE users SET language=$1 WHERE {telegram_id}=$2"
        return await self.execute(sql, language, telegram_id, execute=True)

    async def get_all_telegram_id(self):
        sql = f"SELECT telegram_id FROM users"
        # sql = f"SELECT DISTINCT telegram_id FROM users"
        return await self.execute(sql, fetch=True)
  
    async def get_phone_number(self, telegram_id):
        sql = f"SELECT phone_number FROM users WHERE telegram_id=$1"
        # sql = f"SELECT phone_number FROM users"
        # sql = f"SELECT DISTINCT telegram_id FROM users"
        return await self.execute(sql, telegram_id, fetchval=True)
  
    async def update_user_phone(self, phone_number, telegram_id):
        sql = f"UPDATE users SET phone_number=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone_number, telegram_id, execute=True)
  
    # update bufer column
    async def update_user_bufer(self, bufer, telegram_id):
        sql = f"UPDATE users SET bufer=$1 WHERE telegram_id=$2"
        return await self.execute(sql, bufer, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)




    # --------------------------- user un products jadvali ---------------------------
    async def create_table_products(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NULL,
                price INT NULL,
                discription TEXT NULL,
                photo_id TEXT
                );
            """
        await self.execute(sql, execute=True)

    async def select_products(self):
        sql = "SELECT * FROM Products"
        return await self.execute(sql, fetch=True)
    
    async def select_one_product(self, id):
        sql = "SELECT * FROM Products WHERE id=$1"
        return await self.execute(sql, id, fetchrow=True)
    
    async def count_product(self):
        sql = "SELECT COUNT(*) FROM Products"
        return await self.execute(sql, fetchval=True)

    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)


    # --------------------------- user un baskets(Savatlar) jadvali ---------------------------
    async def create_table_baskets(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Baskets (
                id SERIAL,
                product_id BIGINT REFERENCES products(id),
                user_id BIGINT REFERENCES users(id),
                count INT NOT NULL
                );
            """
        await self.execute(sql, execute=True)
    
    async def add_to_basket(self, product_id, user_id, count):
        sql = "INSERT INTO Baskets (product_id, user_id, count) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, product_id, user_id, count, fetchrow=True)

    async def select_basket(self, user_id):
        sql = "SELECT * FROM Baskets WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)
    
    async def select_product_in_basket(self, user_id):
        sql = "SELECT * FROM Baskets WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)
    
    async def update_basket_product(self, product_id, count, user_id):
        sql = "UPDATE Businesses SET count=$1 WHERE product_id=$2 AND user_id=$3"
        return await self.execute(sql, product_id, count, user_id, execute=True)

    async def delete_product_from_basket(self, user_id):
        sql = "DELETE FROM baskets WHERE user_id=$1"
        return await self.execute(sql, user_id, execute=True)

    async def drop_baskets(self):
        await self.execute("DROP TABLE Baskets", execute=True)


    # --------------------------- user un shoppings data(Oldi-sotti ma'lumotlari) jadvali ---------------------------
    async def create_table_shoppings(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Shoppings (
                id SERIAL,
                data VARCHAR(20) NOT NULL,
                value VARCHAR(20) NOT NULL,
                product_id BIGINT REFERENCES products(id),
                user_id BIGINT REFERENCES users(id)
                );
            """
        await self.execute(sql, execute=True)

    async def select_shopping(self, user_id):
        sql = "SELECT * FROM Shoppings WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def drop_shoppings(self):
        await self.execute("DROP TABLE Shoppings", execute=True)




    # --------------------------- user un kurslar jadvali ---------------------------
    async def create_table_courses(self):
        sql = """
                CREATE TABLE IF NOT EXISTS Courses (
                id SERIAL PRIMARY KEY,
                course_title VARCHAR(255) NULL,
                course_price VARCHAR(50) NULL,
                course_discription TEXT NULL,
                course_plan TEXT NULL,
                course_discount VARCHAR(50) NULL,

                currency VARCHAR(5) NULL,
                course_img_url VARCHAR(255) NULL

                );
            """
        await self.execute(sql, execute=True)

    async def add_course(self, course_title=None, course_price=None, course_discription=None, course_plan=None, course_discount=None, currency=None, course_img_url=None):
        sql = "INSERT INTO Courses (course_title, course_price, course_discription, course_plan, course_discount, currency, course_img_url) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, course_title, course_price, course_discription, course_plan, course_discount, currency, course_img_url, fetchrow=True)

    async def select_courses(self):
        sql = "SELECT * FROM Courses"
        return await self.execute(sql, fetch=True)
    
    async def course_exists(self, course_id):
        sql = "SELECT EXISTS(SELECT 1 FROM Courses WHERE id=$1)"
        return await self.execute(sql, course_id, fetchval=True)
    
    async def count_courses(self):
        sql = "SELECT COUNT(*) FROM Courses"
        return await self.execute(sql, fetchval=True)
    
    
    async def select_one_course(self, id):
        sql = "SELECT * FROM Courses WHERE id=$1"
        return await self.execute(sql, id, fetchrow=True)
    
    async def update_course_data(self, triger, value, id):
        sql = f"UPDATE Courses SET course{triger}=$1 WHERE id=$2"
        return await self.execute(sql, value, id, execute=True)

    async def drop_courses(self):
        await self.execute("DROP TABLE Courses", execute=True)