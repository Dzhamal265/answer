import sqlalchemy as sa
from answer.migrations import metadata

quiz = sa.Table(
    'quiz', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(200), unique=True, nullable=False)
)

question = sa.Table(
    'question', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.Text),
    sa.Column('quiz_id', sa.Integer, sa.ForeignKey('quiz.id')),
)

answer = sa.Table(
    'answer', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('value', sa.Text),
    sa.Column('is_true', sa.Boolean),
    sa.Column('question_id', sa.Integer, sa.ForeignKey('question.id')),
)
