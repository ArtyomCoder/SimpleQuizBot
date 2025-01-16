from .db import pool, execute_select_query


async def get_by_id(question_id: int):
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