from pydantic import BaseModel
from typing import List
from pydantic import ConfigDict

class PollOptionBase(BaseModel):
    id: int
    option_text: str
    vote_count: int

    model_config = ConfigDict(from_attributes=True)

class PollBase(BaseModel):
    id: int
    question: str
    options: List[PollOptionBase]

    model_config = ConfigDict(from_attributes=True)

class VoteRequest(BaseModel):
    poll_id: int
    option_id: int 