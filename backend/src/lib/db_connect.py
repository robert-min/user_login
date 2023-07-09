from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from . import DB_CONNECTION
from model import User


class DBManager:
    """
    Database Manager
    """

    def __init__(self) -> None:
        user = DB_CONNECTION['user']
        passwd = DB_CONNECTION['password']
        host = DB_CONNECTION['host']
        port = DB_CONNECTION['port']
        db = DB_CONNECTION['db']
        charset = DB_CONNECTION['charset']
        engine = create_engine(
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?{charset}",
            echo=False)

        self.session = Session(engine)

    def insert_user_auth(self, email: str, name: str, password: str) -> str:
        try:
            with self.session as session:
                content = User(
                    email=email,
                    name=name,
                    password=password,
                    timestamp=datetime.utcnow()
                )
                session.add(content)
                session.commit()
            return name
        except Exception:
            raise DBManagerError("Failed to insert user auth on DB")

    def delete_user_auth(self, email: str) -> str:
        try:
            with self.session as session:
                sql = select(User).filter(
                    User.email == email).scalars().first()
                user_auth = session.execute(sql)
                if user_auth:
                    session.delete(user_auth)
                session.commit()
            return email
        except Exception:
            raise DBManagerError("Failed to delete user auth on DB")


class DBManagerError(Exception):
    """All DBManager Error"""
