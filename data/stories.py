from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase

class Stories(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = orm.relationship("Users", foreign_keys=[author_id], back_populates="stories")

    review_authors_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_authors = orm.relationship("Users", back_populates="review_stories", foreign_keys=[review_authors_id])

    checked = Column(Boolean, nullable=False, default=False)
