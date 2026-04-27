# Model with base
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash

from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):  # database for users
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permissions = Column(Boolean, nullable=False)
    email = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    news = orm.relationship("News", back_populates="user")  # connection with news table

    stories = orm.relationship(
        "Stories", back_populates="author", foreign_keys="[Stories.author_id]"
    )  # connection with stories table for authors(1 user - a lot of stories)
    review_stories = orm.relationship(
        "Stories",
        back_populates="review_authors",
        foreign_keys="[Stories.review_authors_id]",
    )  # connection with stories table for review authors(1 user - a lot of review stories)

    is_confirmed = Column(Boolean, nullable=False, default=False)
    sessions = orm.relationship("Sessions", back_populates="user")
    email_tokens = orm.relationship("EmailTokens", back_populates="user")
    serialize_rules = ("-password_hash",)

    def set_password(self, password):  # function for hashing and setting password
        self.password_hash = generate_password_hash(password)

    def had_permission(self, permission):  # function for checking permissions
        return permission in self.permissions

    def check_password(self, password):  # function for checking password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):  # for debugging purposes
        return f"<User>{self.id}-{self.login}, {self.permissions}"
