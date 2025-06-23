from pydantic import BaseModel, Field
from typing import List, Optional
import random
from datetime import datetime, timedelta
import uuid


# --- Feature Vectors ---

class FeatureVectors(BaseModel):
    user_features: List[float]
    product_features: List[float]
    contextual_features: List[float]


# --- Fraud Detection Score ---

class FraudDetectionScore(BaseModel):
    model_version: str
    score: float
    confidence: float = Field(ge=0, le=1, description="Confidence level of the fraud score")
    explanation: List[str]


# --- Recommendation Score ---

class Recommendation(BaseModel):
    product_id: str
    score: float = Field(ge=0, le=1, description="Recommendation score between 0 and 1")
    reason: str


class RecommendationScore(BaseModel):
    model_version: str
    recommendations: List[Recommendation]


# --- Churn Prediction ---

class ChurnPredictionScore(BaseModel):
    model_version: str
    churn_probability: float = Field(gt=0, le=1, description="Churn probability between 0 and 1")
    days_to_churn: int
    intervention_recommended: str


# --- Combined Model Scores ---

class ModelScores(BaseModel):
    fraud_detection: FraudDetectionScore
    recommendation: RecommendationScore
    churn_prediction: ChurnPredictionScore


# --- Full ML Context ---

class MLContext(BaseModel):
    feature_vectors: FeatureVectors
    model_scores: ModelScores
