import uuid
import datetime

from typing import List

from sqlalchemy.orm import sessionmaker
from persistance.database import database, engine
from persistance.entities.schema import comment
from persistance.entities.model import Comment

from web.dto.comments import CommentRequest


async def publication_comments(publication_id) -> List[Comment]:
    query = comment.select().where(comment.c.publication_id == publication_id)
    return await database.fetch_all(query)

def create_comment(comment_request: CommentRequest, polarity, publication) -> Comment:
    new_comment = Comment(
        uuid=str(uuid.uuid4()),
        user_uuid=comment_request.user_uuid,
        publication_id=publication.id,
        polarity=polarity,
        body=comment_request.body,
        created_at=datetime.date.today()
    )

    session = sessionmaker(bind=engine)()

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    session.close()

    return new_comment
