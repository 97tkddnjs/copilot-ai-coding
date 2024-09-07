from models import Question
from sqlalchemy.orm import Session
from domain.question import question_schema 
from datetime import datetime

def question_list(db: Session ):

    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list


def get_question(db: Session , id : str):
    _question = db.query(Question).get(id)
    return _question


def create_question(db: Session , question= question_schema.QuestionCreate):
    print('debugging================== ,',question)
    _question = Question(
        title=question.title,
        content=question.content,
        writer = question.writer,
        create_date = datetime.now()
    )
    
    db.add(_question)
    db.commit()

