from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
    job_description: str
    top_k: int = 10


class AssessmentRecommendation(BaseModel):
    name: str
    url: str
    test_type: List[str]
    score: float


class RecommendationResponse(BaseModel):
    recommendations: List[AssessmentRecommendation]