from models.blog import Author
from repositories.base import BaseRepository
from schemas.authors import CreateAuthorSchema, UpdateAuthorSchema

AuthorRepository = BaseRepository[Author, CreateAuthorSchema, UpdateAuthorSchema]

author_repository = BaseRepository(Author)
