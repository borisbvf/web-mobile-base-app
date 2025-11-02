from sqlalchemy import Column, Integer, String, DateTime
from models.base import BaseDBModel

class UserDB(BaseDBModel):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    code = Column(String, nullable=True)