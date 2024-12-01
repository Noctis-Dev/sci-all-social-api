from sqlalchemy import Table, Column, Integer, String, UUID, Enum, Date, ForeignKey

from persistance.database import metadata
from persistance.entities.enums.PublicationType import PublicationType

comment = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True,  autoincrement=True),
    Column("uuid", String(36)),
    Column("user_uuid", String(36)),
    Column("body", String(255)),
    Column("polarity", Integer),
    Column("created_at", Date),
    Column("publication_id", Integer, ForeignKey("publications.id"))
)

m_data = Table(
    "metadata",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uuid", String(36)),
    Column("checked_at", Date),
    Column("user_uuid", String(36)),
    Column("rate", Integer),
)

publications = Table(
    "publications",
    metadata,
    Column("id", Integer, primary_key=True,  autoincrement=True),
    Column("uuid", String(36)),
    Column("user_uuid", String(36)),
    Column("secondary_item_uuid", String(36)),
    Column("body", String(255)),
    Column("type", Enum(PublicationType)),
    Column("created_at", Date),
)

publications_metadata = Table(
    "publications_metadata",
    metadata,
    Column("publication_metadata_id", Integer, primary_key=True, autoincrement=True),
    Column("publication_id", Integer, ForeignKey("publications.id")),
    Column("metadata_id", Integer, ForeignKey("metadata.id")),
)

gemini = Table(
    "gemini_config",
    metadata,
    Column("config_id", Integer, primary_key=True, autoincrement=True),
    Column("access_token", String(1024))
)
