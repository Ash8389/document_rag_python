from aiokafka.admin import NewTopic, AIOKafkaAdminClient


async def create_topic():

    admin =  AIOKafkaAdminClient(
        bootstrap_servers="kafka:9092"
    )

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