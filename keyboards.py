from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def generate_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for i in range(len(answer_options)):
        builder.add(types.InlineKeyboardButton(
            text=answer_options[i],
            callback_data=f"answer_{i}")
        )

    builder.adjust(1)
    return builder.as_markup()