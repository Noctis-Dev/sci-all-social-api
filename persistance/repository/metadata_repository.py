import uuid
import datetime

from sqlalchemy.orm import sessionmaker
from persistance.database import database, engine
from persistance.entities.schema import publications_metadata, m_data
from persistance.entities.model import Metadata, PublicationMetadata

from web.dto.metadata import MetadataRequest
from typing import List


async def get_metadata(publication_id) -> List[Metadata]:
    query = m_data.select().where(publications_metadata.c.publication_id == publication_id)
    return await database.fetch_all(query)


def create_metadata(meta: MetadataRequest, publication_id: int) -> Metadata:
    metadata = Metadata(
        metadata_uuid=str(uuid.uuid4()),
        checked_at=datetime.date.today(),
        user_uuid=meta.user_uuid,
        rate=meta.rate
    )

    session = sessionmaker(bind=engine)()
    session.add(metadata)
    session.commit()
    session.refresh(metadata)

    publication_metadata = PublicationMetadata(
        publication_id=publication_id,
        metadata_id=metadata.id
    )

    session.add(publication_metadata)
    session.commit()
    session.close()

    return metadata
