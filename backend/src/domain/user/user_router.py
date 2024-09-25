from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from datetime import timedelta, datetime
from database import get_db
from domain.user import user_crud, user_schema
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
import jwt
from jwt import PyJWTError

# from domain.user.user_crud import pwd_context 데이터 베이스 상에서 암호화는 아직 안함
router = APIRouter(
    prefix="/api/user",
)


'''
 원래 이렇게 하면 안됨! ㄹㅇ;;;
 SECRET_KEY <- 명시적으로 소스 코드에 넣는 것은 보안위규 위반임
'''
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# REFRESH_TOKEN_EXPIRE_DAYS = 1


# test  정책임
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 2
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c" 
ALGORITHM = "HS256"

# 매개변수로 사용한 token의 값은 FastAPI의 security 패키지에 있는 OAuth2PasswordBearer에 의해 자동으로 매핑
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_crud.create_user(db=db, user_create=_user_create)




@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not (form_data.password == user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token , refresh_token

    access_token  = create_toeken(user.username ,  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token  = create_toeken(user.username , timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "token_type": "bearer",
        
    } 
@router.post("/auth/refresh-token")
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # refresh token이 유효하다면 새로운 access token 발급
        new_access_token = create_toeken(user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"accessToken": new_access_token}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
@router.get("/auth/check-token")
async def check_token(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"message": "Token is valid", "user": user}

def create_toeken(username: str, token_expires : timedelta ):

    _token = jwt.encode(
         {
        "sub": username,
        "exp": datetime.utcnow() + token_expires
        }, SECRET_KEY, algorithm=ALGORITHM
    )

    #   refresh_token = jwt.encode(
    #      {
    #     "sub": username,
    #     "exp": datetime.utcnow() + refresh_token_expires
    #     }, SECRET_KEY, algorithm=ALGORITHM
    # )

    return _token

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
    except PyJWTError:
        raise credentials_exception()
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception()
        return user


# JWT 토큰을 검증하는 함수
def verify_token(token: str):
    try:
        # 토큰 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
        return username  # 유효한 경우 사용자명 반환
    except PyJWTError:
        raise credentials_exception()

# 예외 처리
def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )