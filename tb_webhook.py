import os
from aiogram import Bot, Dispatcher, types
import handlers

import json

# С помощью библиотеки os мы можем получить доступ к параметрам из шага 13 по их имени
API_TOKEN = os.getenv("API_TOKEN")

# Создаем объект бота
bot = Bot(token=API_TOKEN)

# Создаем объект диспетчера
dp = Dispatcher()

# Добавляем роутеры в наш диспетчер
# Роутеры позволяют вынести в отдельные файлу хендлеры (перехватчики событий)
dp.include_router(handlers.router)


async def process_event(event):
    # Передача полученного сообщения от телеграма в бот
    # Конструкция из официальной документации aiogram для произвольного асинхронного фреймворка
    update = types.Update.model_validate(json.loads(event['body']), context={"bot": bot})
    await dp.feed_update(bot, update)

# Точка входа
async def webhook(event, context):
    # Проверка, что прилетел POST-запрос от Telegram
    if event['httpMethod'] == 'POST':
        # Вызываем коррутин изменения состояния нашего бота
        await process_event(event)
        # Возвращаем код 200 успешного выполнения
        return {'statusCode': 200, 'body': 'ok'}

    # Если метод не POST-запрос, то выдаем код ошибки 405
    return {'statusCode': 405}
