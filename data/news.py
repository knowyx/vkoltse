from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase

class News(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'news'
    user_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    user = orm.relationship("Users", back_populates="news")

    def __repr__(self):
        return f"<News id={self.id} title={self.title} content={self.content}>, date={self.date}>, user_id={self.user_id}"