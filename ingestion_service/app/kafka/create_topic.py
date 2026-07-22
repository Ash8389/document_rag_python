from aiokafka.admin import NewTopic, AIOKafkaAdminClient

admin = AIOKafkaAdminClient(
    bootstrap_servers="localhost:9092"
)

async def create_topic():

    await admin.start()

    try:
        topics = await admin.list_topics()

        if "document.chunks" not in topics:

            await admin.create_topics(
                [
                    NewTopic(
                        name="document.chunks",
                        num_partitions=3,
                        replication_factor=1,
                    )
                ]
            )

    finally:
        await admin.close()