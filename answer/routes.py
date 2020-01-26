import pathlib

from aiohttp import web

from answer.quizzes.views import quiz_list, quiz_detail, check_answer

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    add_route('GET', '/quiz_list/', quiz_list, name='quiz_list')
    add_route('GET', '/quiz_detail/{quiz_id}/', quiz_detail, name='quiz_detail')
    add_route('GET', '/answer/{answer_id}/check/', check_answer, name='check_answer')
    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'static'),
        name='static',
    )
