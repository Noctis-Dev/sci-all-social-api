from fastapi import APIRouter, Path, Query
from service import comment_service as service

from web.dto.comments import CommentRequest, CommentResponse
from typing import List

router = APIRouter()


@router.get("", response_model=List[CommentResponse])
async def get_publication_comments(publication_id: str = Query(default=None, max_length=36)) -> List[CommentResponse]:
    return await service.get_publication_comments(publication_id)


@router.post("")
async def create_comment(comment_request: CommentRequest) -> CommentResponse:
    return await service.create_comment(comment_request)
