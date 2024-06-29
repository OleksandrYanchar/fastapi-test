import uuid
from typing import List

from configs.logger import init_logger
from fastapi import HTTPException, status
from repositories.categories import category_repository
from schemas.categories import (
    CategorySchema,
    CreateCategorySchema,
    UpdateCategorySchema,
)
from sqlalchemy.ext.asyncio import AsyncSession

logger = init_logger(__file__)


class CategoryService:
    @staticmethod
    async def create_category(
        category_data: CreateCategorySchema, session: AsyncSession
    ) -> CategorySchema:
        new_category = await category_repository.create(session, obj_in=category_data)
        return CategorySchema(**new_category.dict())

    @staticmethod
    async def update_category(
        category_id: uuid.UUID,
        category_data: UpdateCategorySchema,
        session: AsyncSession,
    ) -> CategorySchema:
        category = await category_repository.get(session, id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        updated_category = await category_repository.update(
            session, db_obj=category, obj_in=category_data
        )
        logger.critical(updated_category.id)
        return CategorySchema(**updated_category.dict())

    @staticmethod
    async def delete_category(
        session: AsyncSession, category_id: uuid.UUID
    ) -> CategorySchema:
        category = await category_repository.get(session, id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        deleted_category = await category_repository.delete(session, db_obj=category)
        return CategorySchema(**deleted_category.dict())

    @staticmethod
    async def get_category(
        session: AsyncSession, category_title: str
    ) -> CategorySchema:
        category = await category_repository.get(session, title=category_title)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        return CategorySchema(**category.dict())

    @staticmethod
    async def get_or_create(
        category_titles: List[str], session: AsyncSession
    ) -> List[uuid.UUID]:
        result_categories = []
        for title in category_titles:
            category = await category_repository.get(session, title=title)
            if category:
                result_categories.append(category.id)
            else:
                new_category = await category_repository.create(
                    session, obj_in={"title": title}
                )
                result_categories.append(new_category.id)
        return result_categories
