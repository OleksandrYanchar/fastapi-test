import uuid
from typing import Optional

from models.blog import Post, PostCategoryTag
from repositories.base import BaseRepository
from schemas.posts import CreatePostSchema, PostCreateRepositorySchema, UpdatePostSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PostRepository(BaseRepository[Post, CreatePostSchema, UpdatePostSchema]):
    def __init__(self, model: Post):
        super().__init__(model)

    async def create_post(
        self, session: AsyncSession, post_data: PostCreateRepositorySchema
    ) -> Post:
        new_post = Post(
            author_id=post_data.author_id,
            title=post_data.title,
            body=post_data.body,
            image=post_data.image,
        )

        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)

        # Adding tags to the post after creation
        for tag_id in post_data.tag_ids:
            post_category_tag = PostCategoryTag(
                postid=new_post.id, tagid=tag_id, categoryid=None
            )
            session.add(post_category_tag)

        # Adding categories to the post after creation
        for category_id in post_data.category_ids:
            post_category_tag = PostCategoryTag(
                postid=new_post.id, tagid=None, categoryid=category_id
            )
            session.add(post_category_tag)

        await session.commit()
        await session.refresh(new_post)

        return new_post

    async def get_post_with_related_data(
        self, session: AsyncSession, post_id: uuid.UUID
    ) -> Optional[Post]:
        result = await session.execute(
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.post_category_tags))
            .filter(Post.id == post_id)
        )
        return result.scalars().first()


post_repository = PostRepository(Post)
