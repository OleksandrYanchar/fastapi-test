import uuid
from typing import List

from models.blog import Tag
from repositories.base import BaseRepository
from schemas.tags import CreateTagSchema, UpdateTagSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TagRepository(BaseRepository[Tag, CreateTagSchema, UpdateTagSchema]):
    def __init__(self, model: Tag):
        super().__init__(model)

    async def get_tag_titles(
        self, session: AsyncSession, tag_ids: List[uuid.UUID]
    ) -> List[str]:
        result = await session.execute(select(Tag.title).where(Tag.id.in_(tag_ids)))
        return [tag for tag in result.scalars().all()]


tag_repository = TagRepository(Tag)
