from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    permissions = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    news = orm.relationship("News", back_populates="user")
    serialize_rules = ('-password_hash',)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def had_permission(self, permission):
        return permission in self.permissions

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User>{self.id}-{self.login}, {self.permissions}'
