from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class CustomModel(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    file_path: Mapped[str] = mapped_column()
