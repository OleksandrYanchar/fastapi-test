import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class CreatePostSchema(BaseModel):
    author_name: str = Field(..., max_length=64)
    title: str = Field(..., max_length=64)
    body: str = Field(..., max_length=1024)
    image: Optional[str] = None
    category_titles: List[str]
    tag_titles: List[str]

    @validator("tag_titles")
    def validate_tag_limit(cls, v):
        if len(v) > 5:
            raise ValueError("A post can have at most 5 tags")
        return v


class UpdatePostSchema(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = Field(None, max_length=1024)
    category_titles: Optional[List[str]] = []
    tag_titles: Optional[List[str]] = []

    class Config:
        from_attributes = True


class PostDataSchema(BaseModel):
    id: uuid.UUID
    author_name: str
    image: Optional[str]
    title: str
    body: str
    created_at: datetime
    updated_at: Optional[datetime]
    categories: List[str] = []
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True


class PostCreateRepositorySchema(BaseModel):
    author_id: uuid.UUID
    title: str = Field(..., max_length=64)
    body: str = Field(..., max_length=1024)
    image: Optional[str] = None
    tag_ids: List[uuid.UUID]
    category_ids: List[uuid.UUID]
