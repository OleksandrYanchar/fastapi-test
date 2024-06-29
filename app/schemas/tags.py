import uuid

from pydantic import BaseModel


class CreateTagSchema(BaseModel):
    title: str


class UpdateTagSchema(BaseModel):
    title: str


class TagSchema(BaseModel):
    id: uuid.UUID
    title: str
