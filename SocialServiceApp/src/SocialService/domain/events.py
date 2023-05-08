from abc import ABC
from dataclasses import dataclass

class Event(ABC):
    pass

@dataclass
class Allocated(Event):
    client_id: int
    service_name: str
    social_service_type: str 

@dataclass
class Deallocated(Event):
    client_id: str
    service_name: str
    qty: int

@dataclass
class NotAvailable(Event):
    service_name: str
