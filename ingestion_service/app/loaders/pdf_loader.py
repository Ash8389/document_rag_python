from langchain_community.document_loaders import PyMuPDFLoader

def pdf_loader(path : str):
    loader = PyMuPDFLoader(file_path=path)
    documents = loader.load()

    return documents