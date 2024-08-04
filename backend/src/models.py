from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
'''
아 어케 만들었더라 기억이 안나는 나의 데배~~
기억이 잘 안나~는 해피

'''


class Question(Base):
    
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    create_date = Column(DateTime, nullable=False)
    


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    answer = Column(Text)
    create_date = Column(DateTime, nullable=False)
    question_id = relationship(Integer, ForeignKey("question.id"))
    

