# Model with base
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        orm)
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


# class for email suggestions tokens
class EmailTokens(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "email-tokens"
    id = Column(Integer, primary_key=True)
    email_key = Column(Integer, nullable=True, unique=True)
    url_key = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(
        Boolean, nullable=False
    )  # 0 - для токенов сброса пароля, 1 - для токенов подтверждения почты
    user = orm.relationship("Users", back_populates="email_tokens")
    sent_date = Column(DateTime)
