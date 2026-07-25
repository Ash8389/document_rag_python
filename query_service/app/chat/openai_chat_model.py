from langchain_openai import ChatOpenAI

from app.chat.chat_model import ChatModel

from app.config.settings import settings

model = ChatOpenAI(
    base_url=settings.groq_base_url,
    api_key=settings.groq_api_key,
    model=settings.groq_chat_model,
    temperature=0.5,
)


# class OpenAiChatModel(ChatModel):

#     def __init__(self):
#         pass

def chat( question, context) :
    messages = [
        (
            "system", "You are expert in documents analyzing give answer according to the context. If answer is not in context then reply 'sorry I can't find it in the document.'",
       ),
        ("human", question+str(context)),
    ]

    result = model.invoke(
        messages
    )

    return result