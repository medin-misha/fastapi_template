from fastapi import APIRouter

from app.modules.rmq_module import RMQMessage, rmq_publisher
from .services.consumer_handler import TEST_EXCHANGE, TEST_QUEUE, TEST_ROUTING_KEY

router = APIRouter(prefix="/test-rmq", tags=["test-rmq"])


@router.post("/ping", response_model=RMQMessage)
async def publish_test_ping() -> RMQMessage:
    return await rmq_publisher.publish(
        event="test.ping",
        payload={"text": "hello from test_rmq_module"},
        queue_name=TEST_QUEUE,
        exchange_name=TEST_EXCHANGE,
        routing_key=TEST_ROUTING_KEY,
    )
