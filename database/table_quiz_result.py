from .db import pool, execute_select_query, execute_update_query


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