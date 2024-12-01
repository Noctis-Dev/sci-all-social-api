from pydantic import BaseModel


class MetadataRequest(BaseModel):
    user_uuid: str
    publication_uuid: str
    rate: int


class MetadataResponse(BaseModel):
    metadata_uuid: int
    user_uuid: str
    rate: int
    checked_at: str
