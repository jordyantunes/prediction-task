from typing import List

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    name: str = Field(..., description="Name to classify")
    n_predictions: int = Field(default=3, description="Number of classes to return")


class PredictionItem(BaseModel):
    value: float
    category: str


class PredictionResponse(BaseModel):
    prediction: List[PredictionItem]
