from db import pool, execute_select_query, execute_update_query


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