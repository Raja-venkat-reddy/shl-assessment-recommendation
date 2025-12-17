from fastapi import FastAPI
from backend.recommender import AssessmentRecommender
from backend.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    AssessmentRecommendation
)

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0"
)

# Load recommender once at startup
recommender = AssessmentRecommender()


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_assessments(request: RecommendationRequest):
    results = recommender.recommend(
        job_description=request.job_description,
        top_k=request.top_k
    )

    recommendations = [
        AssessmentRecommendation(**r) for r in results
    ]

    return RecommendationResponse(
        recommendations=recommendations
    )