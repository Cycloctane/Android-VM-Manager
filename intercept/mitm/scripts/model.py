from typing import Optional
from sqlalchemy import ForeignKey, Text, String, DateTime
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER, BOOLEAN
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class TencentNewsArticle(Base):
    __tablename__ = "tencent_news_articles"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    client_mac: Mapped[str] = mapped_column(CHAR(17), index=True)
    data_created_time: Mapped[datetime] = mapped_column(DateTime)
    article_id: Mapped[str] = mapped_column(CHAR(16), index=True, unique=True)
    title: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(16))
    cate1_name: Mapped[str] = mapped_column(String(4))
    cate2_name: Mapped[str] = mapped_column(String(8))
    article_content: Mapped[str] = mapped_column(Text)
    article_source: Mapped[str] = mapped_column(String(16))
    article_publish_location: Mapped[str] = mapped_column(String(16))
    comments_recorded: Mapped[Optional[bool]] = mapped_column(BOOLEAN(), default=False)


class TencentNewsComment(Base):
    __tablename__ = "tencent_news_comments"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    client_mac: Mapped[str] = mapped_column(CHAR(17), index=True)
    reply_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), index=True, unique=True)
    referer_article_id: Mapped[str] = mapped_column(ForeignKey("tencent_news_articles.article_id",
                                                               onupdate="CASCADE", ondelete="CASCADE"))
    reply_parent_id: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), index=True, nullable=True)
    comment_post_time: Mapped[datetime] = mapped_column(DateTime)
    comment_content: Mapped[str] = mapped_column(Text)
    agree_count: Mapped[int] = mapped_column(INTEGER(unsigned=True))
    user_name: Mapped[str] = mapped_column(String(32))
    user_location: Mapped[str] = mapped_column(String(18))

