from datetime import timedelta
from fastapi import APIRouter, Query, HTTPException, status, Depends, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from sqlalchemy.orm import Session

from crud.user import get_user, create_user, update_code
from schemas.user import UserUpdateCode
import auth
import mail_utils
from dependencies import get_local_session

user_router = APIRouter()

security = HTTPBasic()

@user_router.post("/code_query")
async def send_code(
    email: Annotated[str, Query(title="Email to register new user")],
    db: Session = Depends(get_local_session)
    ):
    email = "".join(letter for letter in email if letter not in ["'", '"'])
    user = get_user(db, email)
    if not user:
        user = create_user(db, email)
    new_code = auth.generate_code()
    user_update = UserUpdateCode(email=email, code=new_code)
    update_code(db, user_update)
    mail_utils.send_code(email, new_code)
    return Response(status_code=status.HTTP_200_OK)

@user_router.get("/token")
async def create_token(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], 
    db: Session = Depends(get_local_session)
    ) -> auth.Token:
    username = credentials.username
    password = credentials.password
    user = get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or code",
            headers={"WWW-Authenticate", "Bearer"}, # type: ignore
        )
    hashed_code = auth.pwd_context.hash(user.code) # type: ignore
    if not auth.pwd_context.verify(password, hashed_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or code",
            headers={"WWW-Authenticate", "Bearer"}, # type: ignore
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return auth.Token(access_token=access_token, token_type="bearer")
