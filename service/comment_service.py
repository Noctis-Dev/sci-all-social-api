import service.publication_service as publication_service
import service.gemini_service as gemini_service

from exeption.entity import EntityNotFoundException

from persistance.repository import comment_repository as repository
from persistance.entities.model import Comment

from web.dto.comments import CommentRequest, CommentResponse
from typing import List


async def get_publication_comments(publication_id) -> List[CommentResponse]:
    publication = await publication_service.get_publication_by_id(publication_id)
    return list(map(_to_response, await repository.publication_comments(publication.id)))


async def create_comment(comment_request: CommentRequest) -> CommentResponse:
    publication = await publication_service.get_publication_by_id(comment_request.publication_uuid)

    if publication is None:
        raise EntityNotFoundException("Publication not found")

    polarity = await gemini_service.get_polarity(comment_request.body)
    return _to_response(repository.create_comment(comment_request, polarity, publication))


def _to_response(comment: Comment) -> CommentResponse:
    return CommentResponse(
        comment_uuid=comment.uuid,
        body=comment.body,
        polarity=comment.polarity,
        created_at=comment.created_at.strftime('%Y-%m-%d'),
        user_uuid=comment.user_uuid,
        publication_id=comment.publication_id,
    )
