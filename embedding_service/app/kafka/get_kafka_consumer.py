from aiokafka import AIOKafkaConsumer

consumer = AIOKafkaConsumer(
    "document.chunks",
    bootstrap_servers="localhost:9092"
)