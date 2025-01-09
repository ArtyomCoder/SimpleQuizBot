from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F, Router

from db import get_quiz_index, update_quiz_index
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


async def get_question(message, user_id):

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


@router.callback_query(F.data.startswith('answer_'))
async def handle_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    user_answer_number = int(callback.data.split('_')[1])
    user_answer = quiz_data[current_question_index]['options'][user_answer_number]
    await callback.message.answer(f'Ваш ответ: {user_answer}')

    if user_answer == correct_option:
        await callback.message.answer("Верно!")
    else:
        await callback.message.answer("Неправильно!")
    
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")