from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunker(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 75
    )

    return splitter.split_documents(docs)