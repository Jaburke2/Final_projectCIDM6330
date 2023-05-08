import logging
from sqlalchemy import (Table, MetaData, Column, Integer, String, ForeignKey, event)
from sqlalchemy.orm import registry, mapper, relationship
from SocialService.domain import models

mapper_registry = registry()
Base = mapper_registry.generate_base()

logger = logging.getLogger(__name__)

metadata = mapper_registry.metadata

socialServices = Table(
   "socialservice",
    metadata,
    Column("service_id", Integer, primary_key=True, autoincrement=True),
    Column("service_name", ForeignKey("service.service_name"), nullable=False),
    Column("social_service_type", String(255), nullable=False),
    Column("qty", Integer, nullable=False)
)

client_table = Table(
    "client_table",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("service_name", String(255), nullable=False),
    Column("social_service_type", String(255), nullable=False),
    Column("client_id", Integer, nullable=False),
    Column("qty", Integer)
)

allocations = Table(
    "allocate_service",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_id", ForeignKey("client_table.client_id")),
    Column("service_id", ForeignKey("socialservice.service_id")),
)

service = Table(
    "service",
    metadata,
    Column("service_name", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

def start_mappers():
    print("starting mappers")
    logger.info("Starting mappers")
    client_mapper = mapper_registry.map_imperatively(models.Client, client_table)
    socialservice_mapper = mapper_registry.map_imperatively(
        models.SocialService,
        socialServices,
        properties={
            "_allocations": relationship(
                client_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        models.Service,
        service,
        properties={"socialservices": relationship(socialservice_mapper)},
    )

@event.listens_for(models.Service, "load")
def receive_load(service, _):
    service.events = []
