import random
from typing import Dict

import aiohttp_jinja2
from aiohttp import web
from sqlalchemy import select

from .tables import quiz, question, answer


@aiohttp_jinja2.template('quiz_list.html')
async def quiz_list(request: web.Request) -> Dict:
    async with request.app.get('db').acquire() as conn:
        cursor = await conn.execute(quiz.select())
        quizzes = await cursor.fetchall()
    return {'quizzes': quizzes}


@aiohttp_jinja2.template('quiz_questions_list.html')
async def quiz_detail(request: web.Request):
    quiz_id = request.match_info.get('quiz_id')
    async with request.app.get('db').acquire() as conn:
        cursor = await conn.execute(
            select([
                question.c.content,
                answer.c.question_id,
                answer.c.value,
                answer.c.id
            ]).select_from(
                question.join(answer)
            ).where(question.c.quiz_id == quiz_id)
        )
        quiz_questions = await cursor.fetchall()
    return {'quiz_questions': quiz_questions}


async def check_answer(request: web.Request):
    answer_id = request.match_info.get('answer_id')

    async with request.app.get('db').acquire() as conn:
        cursor = await conn.execute(
            answer.select().where(answer.c.id == answer_id)
        )
        answer_check_result = await cursor.fetchone()

    if answer_check_result.is_true:
        return web.json_response(data={
            "is_true": answer_check_result.is_true,
            "message": random.choice(["Так держать!", "Отлично!", "Молодец!"])
        })
    else:
        return web.json_response(data={
            "is_true": answer_check_result.is_true,
            "message": random.choice(["Не сдавайся!", "У тебя все получится!"])
        })
