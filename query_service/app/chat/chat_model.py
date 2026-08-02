from abc import ABC, abstractmethod

class ChatModel(ABC):

    @abstractmethod
    def chat(self, query, context) :
        pass