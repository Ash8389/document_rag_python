from aiokafka import AIOKafkaConsumer

consumer = None
async def get_kafka_consumer():
    global consumer
    consumer = AIOKafkaConsumer(
        "document.chunks",
        bootstrap_servers="kafka:9092"
    )

    await consumer.start()

async def stop_consumer():
    global consumer

    if consumer:
        await consumer.stop()