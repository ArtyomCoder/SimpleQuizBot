import aiosqlite
from config import DB_NAME


async def get_current_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_current_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('UPDATE quiz_state SET question_index = (?) WHERE user_id = (?)', (index, user_id))
        # Сохраняем изменения
        await db.commit()


async def create_new_quiz(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, current_result) VALUES (?, ?, ?)', (user_id, 0, 0))
        await db.commit()


async def get_current_quiz_result(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT current_result FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_current_quiz_result(user_id, current_result):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('UPDATE quiz_state SET current_result = (?) WHERE user_id = (?)', (current_result, user_id))
        # Сохраняем изменения
        await db.commit()


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу состояния викторины
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, current_result INTEGER)''')
        # Создаю таблицу результатов пользователей
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_result (user_id INTEGER PRIMARY KEY, previous_result INTEGER)''')
        # Сохраняем изменения
        await db.commit()


async def update_previous_quiz_result(user_id, result):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        await db.execute('INSERT OR REPLACE INTO quiz_result (user_id, previous_result) VALUES (?, ?)', (user_id, result))
        # Сохраняем изменения
        await db.commit()


async def get_previous_quiz_result(user_id):
    # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT previous_result FROM quiz_result WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0