import re
import unicodedata

def clean_text(text : str) -> str :

    text = unicodedata.normalize("NFKC", text)

    text = text.replace("\t", "")

    text = re.sub(r"[ ]+", " ", text)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    text = text.strip()

    return text