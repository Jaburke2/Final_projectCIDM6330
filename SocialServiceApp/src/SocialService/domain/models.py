from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set, Optional
from . import commands, events

@dataclass
class Service:
    service_name: str
    socialservices: List[SocialService]
    version_number: int = 0
    events: List = field(default_factory=list)

    def allocate(self, client: Client) -> Optional[str]:
        try:
            socialservice = next(b for b in sorted(self.socialservices) if b.can_allocate(client))
            socialservice.allocate(client)
            self.version_number += 1
            self.events.append(events.Allocated(client_id=client.client_id, service_name=client.service_name, social_service_type=client.social_service_type))
            return socialservice.service_name
        except StopIteration:
            self.events.append(events.NotAvailable(client.service_name))
            return None

    def change_batch_quantity(self, service_name: str, qty: int):
        socialservice = next(b for b in self.socialservices if b.service_name == service_name)
        socialservice.qty = qty
        while socialservice.available_quantity < 0:
            client = socialservice.deallocate_one()
            self.events.append(events.Deallocated(client.client_id, client.service_name, client.qty))

@dataclass(unsafe_hash=True)
class Client:
    client_id: int
    service_name: str
    social_service_type: str
    qty: int = 1

@dataclass
class SocialService:
    service_name: str
    social_service_type: str
    qty: int
    _allocations: Set[Client] = field(default_factory=set)

    def __post_init__(self):
        self.service_id = hash(self.service_name)

    def allocate(self, client: Client):
        if self.can_allocate(client):
            self._allocations.add(client)

    def deallocate_one(self) -> Client:
        return self._allocations.pop()

    @property
    def allocated_quantity(self) -> int:
        return sum(client.qty for client in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.qty - self.allocated_quantity

    def can_allocate(self, client: Client) -> bool:
        return self.service_name == client.service_name and self.social_service_type == client.social_service_type and self.available_quantity >= client.qty

