from fastapi import Depends
import jwt
from sqlalchemy.orm import Session

from database.session import session_maker
from auth import oauth2_scheme, TokenPayload, SECRET_KEY, ALGORITHM
from models.user import UserDB
from crud.user import get_user

def get_local_session():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()

def get_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM) # type: ignore
        token_data = TokenPayload(**payload)
    except (jwt.PyJWTError) as e:
        raise Exception
    return token_data

def get_current_user(
        db: Session = Depends(get_local_session), 
        token: TokenPayload = Depends(get_token)
        ) -> UserDB:
    user = get_user(db, token.sub) # type: ignore
    if user is None:
        raise Exception
    return user
