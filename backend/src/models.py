from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
'''
아  기억이 안나는 데배~~

'''


class Question(Base):
    
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    writer = Column(String(100))
    create_date = Column(DateTime, nullable=False)
    # Relationship to the Answer model
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    answer = Column(Text)
    create_date = Column(DateTime, nullable=False)
     # Foreign key to the Question model
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    # Relationship to the Question model
    question = relationship("Question", back_populates="answers")
    

