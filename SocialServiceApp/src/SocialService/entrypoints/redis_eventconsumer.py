import json
import logging
import redis

from SocialService import bootstrap, config
from SocialService.domain import commands

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=config.get_redis_host_and_port()["host"],
    port=config.get_redis_host_and_port()["port"],
    db=config.get_redis_host_and_port().get("db", 0),
    decode_responses=True,
)


def main():
    logger.info("Redis pubsub starting")
    bus = bootstrap.bootstrap()
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("socialservice_schedule")

    for m in pubsub.listen():
        handle_change_batch_quantity(m, bus)


def handle_change_batch_quantity(m, bus):
    logger.info("handling %s", m)
    data = json.loads(m["data"])
    cmd = commands.ChangeBatchQuantity(service_name=data["service_name"], qty=data["qty"])
    bus.handle(cmd)


if __name__ == "__main__":
    main()
