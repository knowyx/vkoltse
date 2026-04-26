from data.db_session import SqlAlchemyBase
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, orm
from sqlalchemy_serializer import SerializerMixin


# class for news
class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "news"
    user_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    content = Column(JSON, nullable=False)
    cover_filename = Column(String)
    date = Column(DateTime, nullable=False)
    user = orm.relationship(
        "Users", foreign_keys=[user_id], back_populates="news"
    )  # connection with users table(1 news - 1 user, a lot of news - 1 user)

    def __repr__(self):  # for debugging purposes
        return f"<News id={self.id} title={self.title} content={self.content}>, date={self.date}>, user_id={self.user_id}"
