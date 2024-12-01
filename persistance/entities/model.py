from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from persistance.entities.enums.PublicationType import PublicationType

Base = declarative_base()


class GeminiConfig(Base):
    __tablename__ = 'gemini_config'

    config_id = Column(Integer, primary_key=True, autoincrement=True)
    access_token = Column(String(1024))


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    user_uuid = Column(String(36))
    body = Column(String(255))
    polarity = Column(Integer)
    created_at = Column(Date)
    publication_id = Column(Integer, ForeignKey('publications.id'))


class Metadata(Base):
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    checked_at = Column(Date)
    user_uuid = Column(String(36))
    rate = Column(Integer)


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    user_uuid = Column(String(36))
    secondary_item_uuid = Column(String(36))
    body = Column(String(255))
    type = Column(Enum(PublicationType))
    created_at = Column(Date)


class PublicationMetadata(Base):
    __tablename__ = 'publications_metadata'

    publication_metadata_id = Column(Integer, primary_key=True, autoincrement=True)
    publication_id = Column(Integer, ForeignKey('publications.id'))
    metadata_id = Column(Integer, ForeignKey('metadata.id'))