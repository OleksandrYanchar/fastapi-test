import uuid
from typing import List

from models.blog import Category
from repositories.base import BaseRepository
from schemas.categories import CreateCategorySchema, UpdateCategorySchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository(
    BaseRepository[Category, CreateCategorySchema, UpdateCategorySchema]
):
    def __init__(self, model: Category):
        super().__init__(model)

    async def get_category_titles(
        self, session: AsyncSession, category_ids: List[uuid.UUID]
    ) -> List[str]:
        result = await session.execute(
            select(Category.title).where(Category.id.in_(category_ids))
        )
        return [category for category in result.scalars().all()]


category_repository = CategoryRepository(Category)
