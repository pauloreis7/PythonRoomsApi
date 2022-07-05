from fastapi import APIRouter

sections_router = APIRouter()


@sections_router.get("/sections/{id}")
async def read_section():
    """Get a section"""

    return {"courses": []}


@sections_router.get("/sections/{id}/content-blocks")
async def read_section_content_blocks():
    """Get a section content blocks"""

    return {"courses": []}


@sections_router.get("/content-blocks/{id}")
async def read_content_block():
    """Get a content block"""

    return {"courses": []}
