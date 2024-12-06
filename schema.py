from email_validator import validate_email, EmailNotValidError
import bcrypt
from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, Enum, select, update, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, validates
import os
from dotenv import load_dotenv
load_dotenv()
db = os.getenv("DB")

engine = create_engine(db)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    @validates("email")
    def email_validate(self, key, value):
        try:
            valid_email = validate_email(value, check_deliverability=True)
            return valid_email.email
        except EmailNotValidError:
            raise ValueError

    # Automatically hash the password and store it when the user adds or updates password.
    @validates("password")
    def hash_value(self, key, value):
        return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

    def unhash_value(self, password, hashed_value):
        return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_value.encode("utf-8"))

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}


class Task(Base):
    __tablename__ = "Task"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("todo", "in-progress", "done", name="Todo_enum"), nullable=False)
    createAt: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now())
    updateAt: Mapped[datetime] = mapped_column(DateTime, default=None)

    @validates("status")  # Automatically verify if the status is valid.
    def valid_status(self, key, value):
        allow_status = {"todo", "in-progress", "done"}
        if value not in allow_status:
            raise ValueError
        return value

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}


Base.metadata.create_all(bind=engine)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
