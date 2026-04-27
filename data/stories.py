"""Model with base for store stories, review authors and other data for
displaying and writing stories"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Stories(SqlAlchemyBase, SerializerMixin):
    """Class with stories model"""

    __tablename__ = "stories"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    author_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # 1 story - 1 author, a lot of stories - 1 author
    author = orm.relationship(
        "Users", foreign_keys=[author_id], back_populates="stories"
    )  # connection with users table

    review_authors_id = Column(Integer, ForeignKey("users.id"))
    review_authors = orm.relationship(
        "Users", back_populates="review_stories", foreign_keys=[review_authors_id]
    )  # connection with users table for review authors(1 story - a lot of review authors)
    checked = Column(Boolean, nullable=False, default=False)
