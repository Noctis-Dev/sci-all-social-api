from pydantic import BaseModel


class CommentRequest(BaseModel):
    user_uuid: str
    publication_uuid: str
    body: str


class CommentResponse(BaseModel):
    comment_uuid: str
    user_uuid: str
    body: str
    polarity: int
    created_at: str
