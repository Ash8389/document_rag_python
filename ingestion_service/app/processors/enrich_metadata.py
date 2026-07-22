import uuid

def enrich(chunks):

    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = str(uuid.uuid4())
        chunk.metadata["chunk_idx"] = idx
        chunk.metadata["language"] = "en"
        chunk.metadata["page"] += 1

    return chunks