import asyncio
import uuid
from typing import Optional

from configs.general import AVATARS_DIR
from repositories.categories import category_repository
from repositories.posts import post_repository
from repositories.tags import tag_repository
from schemas.posts import CreatePostSchema, PostCreateRepositorySchema, PostDataSchema
from services.author import AuthorService
from services.categories import CategoryService
from services.tags import TagService
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.files import upload_picture

class PostService:
    @staticmethod
    async def create_post(
        post_data: CreatePostSchema, session: AsyncSession
    ) -> PostDataSchema:
        existing_post = await post_repository.get(session, title=post_data.title)
        if existing_post:
            raise ValueError(
                f"A post with the title '{post_data.title}' already exists."
            )

        author_id = await AuthorService.get_or_create(post_data.author_name, session)
        tags = await TagService.get_or_create(post_data.tag_titles, session)
        category_ids = await CategoryService.get_or_create(
            post_data.category_titles, session
        )

        post_create_data = PostCreateRepositorySchema(
            author_id=author_id,
            title=post_data.title,
            body=post_data.body,
            image=post_data.image,
            tag_ids=[tag.id for tag in tags],
            category_ids=category_ids,
        )

        new_post = await post_repository.create_post(session, post_create_data)

        return await PostService._format_post_to_schema(new_post.id, session)

    @staticmethod
    async def get_post(
        post_id: uuid.UUID, session: AsyncSession
    ) -> Optional[PostDataSchema]:
        post = await post_repository.get(session, id=post_id)
        if not post:
            return None

        return await PostService._format_post_to_schema(post.id, session)

    @staticmethod
    async def _format_post_to_schema(
        post_id: uuid.UUID, session: AsyncSession
    ) -> PostDataSchema:
        post = await post_repository.get_post_with_related_data(session, post_id)
        if not post:
            raise ValueError("Post not found")

        author = post.author
        author_name = author.name

        post_category_tags = post.post_category_tags

        category_ids = [pct.categoryid for pct in post_category_tags if pct.categoryid]
        tag_ids = [pct.tagid for pct in post_category_tags if pct.tagid]

        categories = await category_repository.get_category_titles(
            session, category_ids
        )
        tags = await tag_repository.get_tag_titles(session, tag_ids)

        return PostDataSchema(
            id=post.id,
            author_name=author_name,
            image=post.image,
            title=post.title,
            body=post.body,
            created_at=post.created_at,
            updated_at=post.updated_at,
            categories=categories,
            tags=tags,
        )

    @staticmethod
    async def update_image(
        post_id: uuid.UUID, file_content: bytes, file_name: str, session: AsyncSession
    ) -> PostDataSchema:
        image_task = upload_picture.delay(file_content, file_name, AVATARS_DIR)

        # Using async I/O to wait for the task to complete without blocking
        while not image_task.ready():
            await asyncio.sleep(0.1)

        image_url = image_task.result

        if "Error" in image_url:
            raise ValueError(image_url)

        post = await post_repository.get(session, id=post_id)
        if not post:
            raise ValueError("Post not found")

        post.image = image_url
        await session.commit()
        await session.refresh(post)

        return await PostService._format_post_to_schema(post.id, session)

