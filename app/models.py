from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query")

class AskResponse(BaseModel):
    reasoning: str
    answer: str
    used_tools: list[str] = Field(default_factory=list, description="List of tools used")
