import datetime

from pydantic import BaseModel ,field_validator


class Question(BaseModel):
    id: int
    title: str
    content: str
    writer : str
    create_date: datetime.datetime


class QuestionCreate(BaseModel):

    title: str
    content: str
    writer : str

    @field_validator('title')
    def check_title(cls, v):
        if len(v) < 1: 
            raise ValueError('title must be at least 1 characters')
        return v
    
    @field_validator('content')
    def check_content(cls, v):
        if len(v) < 1:
            raise ValueError('content must be at least 1 characters')
        return v