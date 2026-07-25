from aiokafka import AIOKafkaProducer

producer = None

async def start_producer():
    global producer

    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092"
    )

    await producer.start()


async def stop_producer():
    global producer

    if producer:
        await producer.stop()