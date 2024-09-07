from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_schema,  question_crud
from starlette import status

router = APIRouter(
    prefix="/api/question",
)


@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.question_list(db)
    return _question_list

@router.get("/detail/{id}", response_model=question_schema.Question)
def get_question(db: Session = Depends(get_db)):
    _question =question_crud.get_question(db, id)
    return _question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_question(question : question_schema.QuestionCreate , db: Session = Depends(get_db)):
    print('test==== ',type(question))
    question_crud.create_question(db, question)

