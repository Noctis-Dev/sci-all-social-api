from fastapi import APIRouter
from service import metadata_service as service

from web.dto.metadata import MetadataRequest, MetadataResponse
from typing import List

router = APIRouter()


@router.get("/{publication_id}")
async def get_metadata(publication_id: int) -> List[MetadataResponse]:
    return await service.get_metadata(publication_id)


@router.post("/{publication_id}")
async def create_metadata(publication_id: int, meta: MetadataRequest) -> MetadataResponse:
    return await service.create_metadata(meta, publication_id)
