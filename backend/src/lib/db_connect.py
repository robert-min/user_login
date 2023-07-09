"""DB connection library

MySQLManager:
    - 유저 정보 저장을 위한 EC2 MySQL DB Manager 입니다.
    Functions:
        - insert_user_auth: 유저의 계정 정보를 저장합니다.
        - delete_user_auth: 유저의 계정 정보를 삭제합니다.
        - get_user_auth: 유저의 계정 정보를 가져옵니다.
        - get_all_user_auth_email: DB에 저장된 모든 계정의 이메일을 가져옵니다.

Raises:
    MySQLManagerError: MySQLManager 클래스에서 발생한 오류

"""
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import psycopg2 as pg2
from . import MYSQL_CONNECTION, RDS_CONNECTION
from model import User, Dek


class MySQLManager:
    """
    MySQL database Manager
    """
    def __init__(self) -> None:
        user = MYSQL_CONNECTION['user']
        passwd = MYSQL_CONNECTION['password']
        host = MYSQL_CONNECTION['host']
        port = MYSQL_CONNECTION['port']
        db = MYSQL_CONNECTION['db']
        charset = MYSQL_CONNECTION['charset']
        engine = create_engine(
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?{charset}",
            echo=False, pool_size=10, pool_recycle=500, max_overflow=10)

        self.session = Session(engine)

    def insert_user_auth(self, email: str, name: str, password: str) -> str:
        """Insert user auth info to user_auth table.
        Args:
            email: user email
            name: user name
            password: user decryption password
        
        Return:
            name
            
        Raise:
            Failed to insert user auth on DB.
        """
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
            raise MySQLManagerError("Failed to insert user auth on DB.")

    def delete_user_auth(self, email: str) -> str:
        """Delete user auth info from user_auth table.
        Args:
            email: user email
        
        Return:
            email
            
        Raise:
            Failed to delete user auth on DB.
        """
        try:
            with self.session as session:
                sql = select(User).filter(User.email == email)
                user_auth = session.execute(sql).scalar_one()
                if user_auth:
                    session.delete(user_auth)
                session.commit()
            return email
        except Exception:
            raise MySQLManagerError("Failed to delete user auth on DB.")

    def get_user_auth(self, email: str) -> dict:
        """Get user auth info from user_auth table.
        Args:
            email: user email
        
        Return:
            {"email": email, "name": name, "password": password}
            
        Raise:
            Failed to get user auth on DB.
        """
        try:
            with self.session as session:
                sql = select(User).filter(User.email == email)
                obj = session.execute(sql).scalar_one()
                return {
                    "email": obj.email,
                    "name": obj.name,
                    "password": obj.password
                }
        except Exception:
            raise MySQLManagerError("Failed to get user auth on DB.")

    def get_all_user_auth_email(self) -> list:
        """Get all user auth info from user_auth table.
        Return:
            [email, ...]
            
        Raise:
            Failed to get all user auth email on DB.
        """
        try:
            all_user_auth_email = list()
            with self.session as session:
                sql = select(User)
                for obj in session.execute(sql):
                    all_user_auth_email.append(obj.User.email)
            return all_user_auth_email
        except Exception:
            MySQLManagerError("Failed to get all user auth email on DB.")


class RDSManager:
    """
    RDS Manager
    """
    def __init__(self) -> None:
        user = RDS_CONNECTION['user']
        passwd = RDS_CONNECTION['password']
        host = RDS_CONNECTION['host']
        port = RDS_CONNECTION['port']
        db = RDS_CONNECTION['db']
        charset = RDS_CONNECTION['charset']
        engine = create_engine(
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?{charset}",
            echo=False, pool_size=10, pool_recycle=500, max_overflow=10)

        self.session = Session(engine)

    def insert_user_dek(self, email: str, dek: bytes) -> str:
        try:
            with self.session as session:
                content = Dek(
                    email=email,
                    dek=dek
                )
                session.add(content)
                session.commit()
            return email
        except Exception:
            raise RDSManagerError("Failed to insert user dek on DB.")
        
    def delete_user_dek(self, email: str) -> str:
        try:
            with self.session as session:
                sql = select(Dek).filter(Dek.email == email)
                user_dek = session.execute(sql).scalar_one()
                if user_dek:
                    session.delete(user_dek)
                session.commit()
            return email
        except Exception:
            raise RDSManagerError("Failed to delete user dek on DB.")
    
    def get_user_dek(self, email: str) -> dict:
        try:
            with self.session as session:
                sql = select(Dek).filter(Dek.email == email)
                obj = session.execute(sql).scalar_one()
                return {
                    "email": obj.email,
                    "dek": obj.dek,
                }
        except Exception:
            raise MySQLManagerError("Failed to get user dek on DB.")
    
class MySQLManagerError(Exception):
    """All DBManager Error"""


class RDSManagerError(Exception):
    """All RDSManager Error"""