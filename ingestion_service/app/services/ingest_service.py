from app.loaders.pdf_loader import pdf_loader
from app.processors.cleaner import clean
from app.processors.chunker import chunker
from app.processors.enrich_metadata import enrich
from app.kafka.kafka_producer import produce

class IngestService:

    async def inget_service(self, path):
        docs = pdf_loader(path)

        docs = clean(docs)

        chunks = chunker(docs)

        chunks = enrich(chunks)

        
        # for i, chunk in enumerate(chunks):
        #     print(f"chunk {i}")
        #     print(f"chunk metadata: {chunk.metadata}")
        #     print(f"chunk content: {chunk.page_content}")
        #     print("-"*20)

        await produce(chunks=chunks)
