from app.processors.text_cleaner import clean_text

def clean(docs):

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    return docs
