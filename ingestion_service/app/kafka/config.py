from aiokafka import AIOKafkaProducer

producer = AIOKafkaProducer(
    bootstrap_servers="localhost:9092"
)