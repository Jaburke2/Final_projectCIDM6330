from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from SocialService.domain import commands, events, models
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from SocialService.adapters import notifications
    from . import unit_of_work

class InvalidService(Exception):
    pass

def add_service(
    cmd: commands.CreateService,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        service = uow.services.get(service_name=cmd.service_name)
        if service is None:
            service = models.Service(cmd.service_name, socialservices=[])
            uow.services.add(service)
            service.socialservices.append(models.SocialService(cmd.service_name, cmd.social_service_type, cmd.qty))
        else:
            print("Already Available")
        uow.commit()

def allocate(
    cmd: commands.AllocateService,
    uow: unit_of_work.AbstractUnitOfWork,
):
    client = models.Client(cmd.client_id, cmd.service_name, cmd.social_service_type, 1)
    with uow:
        service = uow.services.get(service_name=client.service_name)
        if service is None:
            raise InvalidService(f"Invalid service {client.service_name}")
        service.allocate(client)
        uow.commit()

def reallocate(
    event: events.Deallocated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    allocate(commands.Allocate(**asdict(event)), uow=uow)

def change_batch_quantity(
    cmd: commands.ChangeBatchQuantity,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        service = uow.services.get_by_batchref(service_name=cmd.service_name)
        service.change_batch_quantity(qty=cmd.qty)
        uow.commit()

def publish_allocated_event(
    event: events.Allocated,
    publish: Callable,
):
    publish("service_allocated", event)

def send_out_of_stock_notification(
    event: events.NotAvailable,
    notifications: notifications.AbstractNotifications,
):
    notifications.send(
        "stock@made.com",
        f"Service not available for {event.service_name}",
    )

EVENT_HANDLERS = {
    events.Allocated: [publish_allocated_event],
    events.Deallocated: [reallocate],
    events.NotAvailable: [send_out_of_stock_notification],
}

COMMAND_HANDLERS = {
    commands.CreateService: add_service,
    commands.AllocateService: allocate,
    commands.ChangeBatchQuantity: change_batch_quantity,
}