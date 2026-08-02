from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_redis import RedisChatMessageHistory

from app.chat.chat_model import ChatModel
from app.config.settings import settings




class OpenAiChatModel(ChatModel):

    def __init__(self):
        self.model = ChatOpenAI(
            base_url=settings.groq_base_url,
            api_key=settings.groq_api_key,
            model=settings.groq_chat_model,
            temperature=0.5,
        )

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert in document analysis. Answer only from the provided context."
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}\n\nContext:\n{context}")
        ])
        
        chain = prompt | self.model
        
        self.chat_chain = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )
    
    def get_session_history(self, session_id: str):
        history = RedisChatMessageHistory(
            session_id=session_id,
            redis_url= f"redis://{settings.redis_host}:{settings.redis_port}",
            key_prefix="chat:",
            ttl=3600,
        )

        if len(history.messages) > 10:
            history.clear()
            history.add_messages(history.messages[-10:])

        
        return history

        


    def chat(self, question, context) :

        result = self.chat_chain.invoke(
            {
                "question": question,
                "context": "\n\n".join(context)
            },
            config={
                "configurable": {
                    "session_id": "session_id"
                }
            }
        )

        return result