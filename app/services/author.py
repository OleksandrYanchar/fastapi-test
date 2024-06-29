import uuid

from configs.logger import init_logger
from fastapi import HTTPException, status
from repositories.authors import author_repository
from schemas.authors import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from sqlalchemy.ext.asyncio import AsyncSession

logger = init_logger(__file__)


class AuthorService:
    @staticmethod
    async def create_author(
        author_data: CreateAuthorSchema, sessoin: AsyncSession
    ) -> AuthorSchema:
        new_author = await author_repository.create(sessoin, obj_in=author_data)
        return AuthorSchema(**new_author.dict())

    @staticmethod
    async def update_author(
        author_id: uuid.UUID, author_data: UpdateAuthorSchema, sessoin: AsyncSession
    ) -> AuthorSchema:
        author = await author_repository.get(sessoin, id=author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="author not found",
            )
        new_author = await author_repository.update(
            sessoin, db_obj=author, obj_in=author_data
        )
        return AuthorSchema(**new_author.dict())

    @staticmethod
    async def delete_author(
        session: AsyncSession, author_id: uuid.UUID
    ) -> AuthorSchema:
        author = await author_repository.get(session, id=author_id)
        deleted_author = await author_repository.delete(session, db_obj=author)
        return AuthorSchema(**deleted_author.dict())

    @staticmethod
    async def get_author(session: AsyncSession, author_name: str) -> AuthorSchema:
        author = await author_repository.get(session, name=author_name)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found",
            )
        return AuthorSchema(**author.dict())

    @staticmethod
    async def get_or_create(author_name: str, session: AsyncSession) -> uuid.UUID:
        author = await author_repository.get(session, name=author_name)
        if author:
            return author.id
        else:
            new_author = await author_repository.create(
                session, obj_in={"name": author_name}
            )
            return new_author.id
