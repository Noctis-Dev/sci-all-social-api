from enum import Enum
from typing import List
from pydantic import BaseModel, constr


class PublicationType(str, Enum):
    COMMON = "common"
    STREAM = "stream"
    SCI_ARTICLE = "sci_article"


class PublicationRequest(BaseModel):
    body: str
    type: PublicationType
    resource: str
    resource_type: str
    secondary_item_uuid: str
    user_uuid: str


class PublicationResponse(BaseModel):
    publication_uuid: str
    body: str
    type: PublicationType
    secondary_item_uuid: str
    created_at: str
    user_uuid: str


class ChartData(BaseModel):
    polarity: float
    month: int
    day: int
    date: str


class PolarityFrom(BaseModel):
    publication: str
    publication_uuid: str
    polarity: List[ChartData]
    forecast: List[float] = None


class PublicationPolarityResponse(BaseModel):
    data: List[PolarityFrom]


class ChatbotSomeRequest(BaseModel):
    body: str
    publication_uuid: str


class ChatbotSomeResponse(BaseModel):
    response: str
