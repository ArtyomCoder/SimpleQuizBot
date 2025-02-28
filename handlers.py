from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F, Router

from db import (
    get_current_quiz_index, 
    update_current_quiz_index,
    get_current_quiz_result,
    update_current_quiz_result,
    get_previous_quiz_result,
    update_previous_quiz_result,
    create_new_quiz,
)
from quiz_data import quiz_data
from keyboards import generate_start_keyboard, generate_options_keyboard

router = Router()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = generate_start_keyboard()
    await message.answer("Добро пожаловать в квиз!", reply_markup=kb)


# Хэндлер на команду /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)


# Хэндлер на команду /result
@router.message(F.text=="Прошлый результат")
@router.message(Command("result"))
async def cmd_previous_quiz_result(message: types.Message):
    previous_result = await get_previous_quiz_result(message.from_user.id)
    await message.answer(f"Счет прошлой викторины: {previous_result}")


async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_current_quiz_index(user_id)
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts)
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    await create_new_quiz(user_id)
    await get_question(message, user_id)


# обработчик ответа на вопрос | я объединил две функции в одну
@router.callback_query(F.data.startswith('answer_'))
async def handle_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # номер вопроса и номер правильного ответа
    current_question_index = await get_current_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    # ответ пользователя и его номер ответа
    user_answer_number = int(callback.data.split('_')[1])
    user_answer = quiz_data[current_question_index]['options'][user_answer_number]
    # печатаю ответ пользователя
    await callback.message.answer(f'Ваш ответ: {user_answer}')

    # сравниваю ответ пользователя с правильным
    if user_answer_number == correct_option:
        await callback.message.answer("Верно!")
        # запрашиваю и обновляю результат актуальной викторины
        quiz_result = await get_current_quiz_result(callback.from_user.id)
        quiz_result += 1
        await update_current_quiz_result(callback.from_user.id, quiz_result)
    else:
        await callback.message.answer("Неправильно!")
    
    # обновляю номер актуального вопроса
    current_question_index += 1
    await update_current_quiz_index(callback.from_user.id, current_question_index)

    # проверяю на окончание викторины
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        # вывожу результат викторины
        final_quiz_result = await get_current_quiz_result(callback.from_user.id)
        await callback.message.answer(
            f"Это был последний вопрос. Квиз завершен!\nВаш счет: {final_quiz_result}")
        # записываю результат викторины в отдельную таблицу
        await update_previous_quiz_result(callback.from_user.id, final_quiz_result)