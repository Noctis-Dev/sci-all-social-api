import uuid
import datetime

from typing import List
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from persistance.database import database, engine
from persistance.entities.schema import publications, comment
from persistance.entities.model import Publication
from web.dto.publication import PublicationRequest, PublicationPolarityResponse


async def find_all_publications(type) -> List[Publication]:
    if type is None:
        query = publications.select()
    else:
        query = publications.select().where(publications.c.type == type)
    return await database.fetch_all(query)


async def find_all_user_publications(userUuid, type) -> List[Publication]:
    if type is None:
        query = publications.select()
    else:
        query = publications.select().where(publications.c.type == type, publications.c.user_uuid == userUuid)
    return await database.fetch_all(query)


def get_publication_polarity(author: str):
    session = sessionmaker(bind=engine)()

    sql_query = text("""
        SELECT 
            AVG(c.polarity) AS DayPolarity, 
            DATE(c.created_at) as date,
            DAY(c.created_at) AS day, 
            MONTH(c.created_at) AS month, 
            p.body AS publication, 
            p.uuid AS publication_uuid
        FROM comments c JOIN publications p ON c.publication_id = p.id
        WHERE p.user_uuid = :user_uuid
        GROUP BY DATE(c.created_at), DAY(c.created_at), MONTH(c.created_at), p.body, p.uuid
        ORDER BY day, month;
    """)

    return session.execute(sql_query, {'user_uuid': author})


async def find_publication_by_id(publication_id) -> Publication:
    query = publications.select().where(publications.c.uuid == publication_id)
    return await database.fetch_one(query)


def create_publications(publication_request: PublicationRequest) -> Publication:
    new_publication = Publication(
        uuid=str(uuid.uuid4()),
        user_uuid=publication_request.user_uuid,
        secondary_item_uuid=publication_request.secondary_item_uuid,
        body=publication_request.body,
        type=publication_request.type.name,
        created_at=datetime.date.today()
    )

    session = sessionmaker(bind=engine)()

    session.add(new_publication)
    session.commit()
    session.refresh(new_publication)

    session.close()

    return new_publication
