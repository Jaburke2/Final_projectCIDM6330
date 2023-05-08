import json
import logging
from dataclasses import asdict
import redis

from SocialService import config
from SocialService.domain import events

logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=config.get_redis_host_and_port()["host"],
    port=config.get_redis_host_and_port()["port"],
    db=config.get_redis_host_and_port().get("db", 0),
    decode_responses=True,
)


def publish(channel: str, event: events.Event):
    logger.info("publishing: channel=%s, event=%s", channel, event)
    redis_client.publish(channel, json.dumps(asdict(event)))
