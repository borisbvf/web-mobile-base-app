from sqlalchemy.orm import Session
from models.user import UserDB
from schemas.user import UserUpdateCode
from datetime import datetime

def get_user(db: Session, email: str) -> UserDB | None:
    return db.query(UserDB).filter(UserDB.email == email).first()

def create_user(db: Session, email: str) -> UserDB:
    obj_db = UserDB(email=email)
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db

def update_code(db: Session, user: UserUpdateCode) -> UserDB:
    obj_db = get_user(db, user.email)
    if obj_db is None:
        raise Exception
    obj_db.code = user.code # type: ignore
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db