from pydantic import BaseModel
from typing import List, Optional


class GroupData(BaseModel):
    name: str
    values: List[float]


class AnalysisRequest(BaseModel):
    groups: List[GroupData]
    method: str
    options: Optional[dict] = None