import uuid

from pydantic import BaseModel


class CreateAuthorSchema(BaseModel):
    name: str


class UpdateAuthorSchema(BaseModel):
    name: str


class AuthorSchema(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True
