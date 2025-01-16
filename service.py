from db import pool, execute_select_query, execute_update_query
from keyboards import generate_options_keyboard


async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_current_quiz_index(user_id)
    opts = await get_options(current_question_index)
    kb = generate_options_keyboard(opts)
    question_text = await get_question_by_id(current_question_index)['question_text']
    await message.answer(f"{question_text}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    await create_new_quiz(user_id)
    await get_question(message, user_id)


# quiz_state
async def create_new_quiz(user_id):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;
        DECLARE $current_result AS Uint64;

        UPSERT INTO `quiz_state` (`user_id`, `question_index`, `current_result`)
        VALUES ($user_id, $question_index, $current_result);
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=0,
        current_result=0,
    )


async def get_current_quiz_index(user_id):
    get_quiz_state = f"""
        DECLARE $user_id AS Uint64;

        SELECT question_index
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_quiz_state, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["question_index"] is None:
        return 0
    return results[0]["question_index"]


async def update_current_quiz_index(user_id, index):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;

        UPDATE `quiz_state`
        SET question_index = $question_index
        WHERE user_id == $user_id;
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=index,
    )


async def get_current_quiz_result(user_id):
    get_quiz_state = f"""
        DECLARE $user_id AS Uint64;

        SELECT current_result
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_quiz_state, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["current_result"] is None:
        return 0
    return results[0]["current_result"]


async def update_current_quiz_result(user_id, current_result):    
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $current_result AS Uint64;

        UPDATE `quiz_state`
        SET current_result = $current_result
        WHERE user_id == $user_id;
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        current_result=current_result,
    )


# quiz_result
async def update_previous_quiz_result(user_id, result):
    set_quiz_result = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $previous_result AS Uint64;

        UPSERT INTO `quiz_result` (`user_id`, `previous_result`)
        VALUES ($user_id, $previous_result);

        UPDATE `quiz_result`
        SET previous_result = $previous_result
        WHERE user_id == $user_id;
    """

    execute_update_query(
        pool,
        set_quiz_result,
        user_id=user_id,
        previous_result=result,
    )


async def get_previous_quiz_result(user_id):
    get_quiz_result = f"""
        DECLARE $user_id AS Uint64;

        SELECT previous_result
        FROM `quiz_result`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_quiz_result, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["previous_result"] is None:
        return 0
    return results[0]["previous_result"]


# quiz_questions
async def get_question_by_id(question_id: int):
    get_question_info = f"""
        DECLARE $question_id AS Uint64;

        SELECT *
        FROM `quiz_questions`
        WHERE question_id == $question_id;
    """
    results = execute_select_query(pool, get_question_info, question_id=question_id)
    return results[0]


async def get_question_count():
    get_question_info = f"""
        SELECT COUNT(*) AS count
        FROM quiz_questions;
    """
    results = execute_select_query(pool, get_question_info)
    return results[0]['count']

async def get_options(question_id: int):
    get_options = f"""
        DECLARE $question_id AS Uint64;

        SELECT *
        FROM `quiz_options`
        WHERE question_id == $question_id;
    """
    results = execute_select_query(pool, get_options, question_id=question_id)
    return [r['option_text'] for r in results]