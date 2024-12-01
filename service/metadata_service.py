from persistance.repository import metadata_repository as repository
from persistance.entities.model import Metadata

from web.dto.metadata import MetadataRequest, MetadataResponse
from typing import List


async def get_metadata(publication_id) -> List[MetadataResponse]:
    metadata = await repository.get_metadata(publication_id)
    return list(map(_to_response, metadata))


def create_metadata(meta: MetadataRequest, publication_id) -> MetadataResponse:
    return _to_response(repository.create_metadata(meta, publication_id))


def _to_response(metadata: Metadata) -> MetadataResponse:
    return MetadataResponse(
        metadata_uuid=metadata.id,
        user_uuid=metadata.user_uuid,
        rate=metadata.rate,
        checked_at=metadata.checked_at,
    )
