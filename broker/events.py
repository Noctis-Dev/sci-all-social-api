from pydantic import BaseModel


class PublicationResourceEvent(BaseModel):
    resource: str
    resource_type: str
    owner_type: str
    owner_resource_type: str
    owner_uuid: str
