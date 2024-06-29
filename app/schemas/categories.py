import uuid

from pydantic import BaseModel


class CreateCategorySchema(BaseModel):
    title: str


class UpdateCategorySchema(BaseModel):
    title: str


class CategorySchema(BaseModel):
    id: uuid.UUID
    title: str
