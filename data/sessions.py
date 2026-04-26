from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin


class Sessions(SqlAlchemyBase, SerializerMixin):  # class for browser sessions
    __tablename__ = "Sessions"
    id = Column(Integer, primary_key=True)
    session_key = Column(String, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"))  # 1 session - 1 user
    user = orm.relationship("Users", back_populates="sessions")
    auth_date = Column(DateTime)
    user_agent = Column(String)
