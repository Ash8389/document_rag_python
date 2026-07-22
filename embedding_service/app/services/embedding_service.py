# from app.kafka.consumer import consume_chunks
from app.processors.embed import embed_text
from app.qdrant.insert_chunks import insert_chunks


async def embedding_service(chunks):

    contents = [chunk["content"] for chunk in chunks]

    embeddings =  await embed_text(contents)

    insert_chunks(embeddings=embeddings, chunks=chunks)

    print("INSERTED")