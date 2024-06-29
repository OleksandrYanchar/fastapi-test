from api.v1.blog.authors import router as authors_router
from api.v1.blog.categories import router as categories_router
from api.v1.blog.posts import router as posts_router
from api.v1.blog.tags import router as tags_router
from fastapi import APIRouter

router = APIRouter(
    prefix="/v1",
)

router.include_router(authors_router)
router.include_router(tags_router)
router.include_router(categories_router)
router.include_router(posts_router)
