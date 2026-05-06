from pydantic import BaseModel
from typing import Optional

class CodeReviewRequest(BaseModel):
    code: str
    language: Optional[str] = "python"
    context: Optional[str] = None

class ReviewIssue(BaseModel):
    type: str
    severity: str
    line: Optional[str] = None
    description: str
    suggestion: str

class CodeReviewResponse(BaseModel):
    summary: str
    issues: list[ReviewIssue]
    score: int
    improved_code: Optional[str] = None
