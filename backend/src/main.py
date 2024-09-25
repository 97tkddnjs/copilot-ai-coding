from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.question import question_router
from domain.user import user_router
app = FastAPI()


origins = [
    "http://127.0.0.1:5173",
       "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"message": "안녕하세요 ~~"}

'''
데이터 저장해야 될 것 같음
'''

app.include_router(question_router.router)
app.include_router(user_router.router)


if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)