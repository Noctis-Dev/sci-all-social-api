from fastapi import APIRouter, Query
from web.dto.publication import PublicationType
from service import publication_service as service

from typing import List
from web.dto.publication import (
    PublicationRequest,
    PublicationResponse,
    PublicationPolarityResponse,
    ChatbotSomeRequest,
    ChatbotSomeResponse
)

router = APIRouter()


@router.get("", response_model=List[PublicationResponse])
async def get_publications(type: PublicationType = Query(default="sci_article", max_length=50)) -> List[PublicationResponse]:
    return await service.get_publications(type)


@router.get("/user/{userUuid}", response_model=List[PublicationResponse])
async def get_user_publications(userUuid: str, type: PublicationType = Query(default="sci_article", max_length=50)) -> List[PublicationResponse]:
    return await service.get_user_publications(userUuid, type)


@router.get("/polarity", response_model=PublicationPolarityResponse)
def get_publications_polarity(user: str = Query(default=None, max_length=36)):
    return service.publication_polarity(user)


@router.post("", response_model=PublicationResponse)
async def create_publication(request: PublicationRequest) -> PublicationResponse:
    return await service.create_publication(request)


@router.post("chatbot", response_model=ChatbotSomeResponse)
async def request_to_chatbot(request: ChatbotSomeRequest):
    return await service.chatbot(request)
