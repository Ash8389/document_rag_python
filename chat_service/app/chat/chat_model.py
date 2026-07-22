from abc import ABC, abstractmethod

class ChatModel(ABC):

    @abstractmethod
    def chat(query, context) :
        pass