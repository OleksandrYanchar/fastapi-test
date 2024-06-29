import uuid
from typing import List, Optional

from configs.db import Base
from models.annotes import created_at, intpk, unique_str_64, updated_at, uuidpk
from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[uuidpk]
    name: Mapped[unique_str_64]
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

    __table_args__ = (Index("author_name_index", "name"),)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuidpk]
    title: Mapped[unique_str_64]
    post_category_tags: Mapped[List["PostCategoryTag"]] = relationship(
        "PostCategoryTag", back_populates="category"
    )

    __table_args__ = (Index("category_title_index", "title"),)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuidpk]
    title: Mapped[unique_str_64]
    post_category_tags: Mapped[List["PostCategoryTag"]] = relationship(
        "PostCategoryTag", back_populates="tag"
    )

    __table_args__ = (Index("tag_title_index", "title"),)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuidpk]
    author_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("authors.id", ondelete="CASCADE")
    )

    author: Mapped["Author"] = relationship("Author", back_populates="posts")

    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[unique_str_64]
    body: Mapped[str] = mapped_column(String(1024), nullable=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    post_category_tags: Mapped[List["PostCategoryTag"]] = relationship(
        "PostCategoryTag", back_populates="post"
    )

    __table_args__ = (Index("post_title_index", "title"),)


class PostCategoryTag(Base):
    __tablename__ = "posts_categories_tags"

    id: Mapped[intpk] = mapped_column(Integer, primary_key=True, autoincrement=True)

    postid: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    post: Mapped["Post"] = relationship("Post", back_populates="post_category_tags")

    categoryid: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
    )
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="post_category_tags"
    )

    tagid: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), nullable=True
    )
    tag: Mapped[Optional["Tag"]] = relationship(
        "Tag", back_populates="post_category_tags"
    )

    __table_args__ = (
        Index("posts_categories_tags_index", "postid", "categoryid", "tagid"),
    )
