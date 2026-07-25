from pydantic import BaseModel

class LlmResponse(BaseModel) :
    answer: str
    model_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int