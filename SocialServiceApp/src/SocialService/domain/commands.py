from dataclasses import dataclass
from typing import Optional

class Command:
    pass


@dataclass
class CreateService(Command):
    service_name: str
    social_service_type: str
    qty: int


@dataclass
class AllocateService(Command):
    client_id: int
    service_name: str
    social_service_type: str

@dataclass
class ChangeBatchQuantity(Command):
    service_name: str
    qty: int
