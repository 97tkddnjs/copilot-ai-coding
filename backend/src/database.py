from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import contextlib

from dotenv import load_dotenv
import os

load_dotenv()

class DbBase:
    def __init__(self):
        self.address = None
        self.engine = None

    def get_mysql_address(self):
        user_id = os.getenv("MYSQL_USER")
        user_pw = os.getenv("MYSQL_PASSWORD")
        mysql_address = os.getenv("MYSQL_ADDRESS")
        mysql_port = os.getenv("MYSQL_PORT")
        db_name = os.getenv("MYSQL_DATABASE")
        return f"mysql+pymysql://{user_id}:{user_pw}@{mysql_address}:{mysql_port}/{db_name}?charset=utf8"

    def __enter__(self):
        self.engine = create_engine(self.get_mysql_address(), encoding='utf-8', echo=False)
        session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = session()
        return self

    def __exit__(self, type, value, traceback):
        if self.session:
            self.session.close()
        
Base = declarative_base()


def get_db():
    yield DbBase().session()
