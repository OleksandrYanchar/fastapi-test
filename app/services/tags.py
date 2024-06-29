import uuid
from typing import List

from configs.logger import init_logger
from fastapi import HTTPException, status
from repositories.tags import tag_repository
from schemas.tags import CreateTagSchema, TagSchema, UpdateTagSchema
from sqlalchemy.ext.asyncio import AsyncSession

logger = init_logger(__file__)


class TagService:
    @staticmethod
    async def create_tag(tag_data: CreateTagSchema, sessoin: AsyncSession) -> TagSchema:
        new_tag = await tag_repository.create(sessoin, obj_in=tag_data)
        return TagSchema(**new_tag.dict())

    @staticmethod
    async def update_tag(
        tag_id: uuid.UUID, tag_data: UpdateTagSchema, sessoin: AsyncSession
    ) -> TagSchema:
        tag = await tag_repository.get(sessoin, id=tag_id)
        new_tag = await tag_repository.update(sessoin, db_obj=tag, obj_in=tag_data)
        logger.critical(new_tag.id)
        return TagSchema(**new_tag.dict())

    @staticmethod
    async def delete_tag(session: AsyncSession, tag_id: uuid.UUID) -> TagSchema:
        tag = await tag_repository.get(session, id=tag_id)
        deleted_tag = await tag_repository.delete(session, db_obj=tag)
        return TagSchema(**deleted_tag.dict())

    @staticmethod
    async def get_tag(session: AsyncSession, tag_title: str) -> TagSchema:
        tag = await tag_repository.get(session, title=tag_title)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="tag not found",
            )
        return TagSchema(**tag.dict())

    @staticmethod
    async def get_or_create(
        tag_titles: List[str], session: AsyncSession
    ) -> List[TagSchema]:
        result_tags = []
        for title in tag_titles:
            tag = await tag_repository.get(session, title=title)
            if tag:
                result_tags.append(tag)
            else:
                new_tag = await tag_repository.create(session, obj_in={"title": title})
                result_tags.append(new_tag)
        return result_tags
