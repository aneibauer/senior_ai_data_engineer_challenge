from pydantic import BaseModel, Field
from typing import List, Optional
import random
from datetime import datetime, timedelta
import uuid

from data_generator.models.ml import (
    FeatureVectors,
    FraudDetectionScore,
    Recommendation,
    RecommendationScore,
    ChurnPredictionScore,
    ModelScores,
    MLContext
)

# -- ML Factories --

def make_feature_vectors() -> FeatureVectors:
    return FeatureVectors(
        user_features=[round(random.uniform(0, 1), 4) for _ in range(10)],
        product_features=[round(random.uniform(0, 1), 4) for _ in range(10)],
        contextual_features=[round(random.uniform(0, 1), 4) for _ in range(5)]
    )

def make_fraud_detection_score() -> FraudDetectionScore:
    return FraudDetectionScore(
        model_version=f"fd_{random.randint(1, 5)}.0",
        score=round(random.uniform(0, 1), 4),
        confidence=round(random.uniform(0.5, 1.0), 3),
        explanation=[random.choice([
            "Unusual location", "High order value", "Velocity flag", "Device mismatch", "Known fraud pattern"
        ]) for _ in range(random.randint(1, 3))]
    )

def make_recommendation() -> Recommendation:
    return Recommendation(
        product_id=f"prod_{uuid.uuid4().hex[:8]}",
        score=round(random.uniform(0, 1), 3),
        reason=random.choice([
            "Similar users bought", "Frequently viewed together", "Personalized for you", "Trending product"
        ])
    )

def make_recommendations(n=5) -> list[Recommendation]:
    return [make_recommendation() for _ in range(n)]

def make_recommendation_score() -> RecommendationScore:
    return RecommendationScore(
        model_version=f"rec_{random.randint(1, 3)}.0",
        recommendations=make_recommendations(random.randint(3, 7))
    )

def make_churn_prediction_score() -> ChurnPredictionScore:
    return ChurnPredictionScore(
        model_version=f"churn_{random.randint(1, 3)}.0",
        churn_probability=round(random.uniform(0.01, 1.0), 3),
        days_to_churn=random.randint(1, 90),
        intervention_recommended=random.choice([
            "Send retention email", "Offer discount", "No action", "Call customer"
        ])
    )

def make_model_scores() -> ModelScores:
    return ModelScores(
        fraud_detection=make_fraud_detection_score(),
        recommendation=make_recommendation_score(),
        churn_prediction=make_churn_prediction_score()
    )

def make_ml_context() -> MLContext:
    return MLContext(
        feature_vectors=make_feature_vectors(),
        model_scores=make_model_scores()
    )
