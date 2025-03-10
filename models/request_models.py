from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    text: str
    num_sentences: int = 1
