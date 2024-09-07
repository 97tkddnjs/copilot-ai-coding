실행방법   
 uvicorn main:app --reload

 ## 테이블 교체 혹은 바뀔 시 

### 초기 생성시
alembic init migrations


### 변경 할 시
alembic revision --autogenerate
alembic upgrade head