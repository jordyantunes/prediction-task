import os
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from scripts.predict import predict

MODEL_PATH = os.environ.get("MODEL_PATH", "experiments/weights.pt")
PARAMS_PATH = os.environ.get("MODEL_PATH", "experiments/params.json")

app = FastAPI()


class PredictionRequest(BaseModel):
    name: str = Field(..., description="Name to classify")
    n_predictions: int = Field(default=3, description="Number of classes to return")


class PredictionItem(BaseModel):
    value: float
    category: str


class PredictionResponse(BaseModel):
    prediction: List[PredictionItem]


@app.get("/")
def read_root():
    return {"message": "Service is up"}


@app.post("/predict")
def predict_text(request: PredictionRequest) -> PredictionResponse:
    prediction = predict(
        name=request.name,
        n_predictions=request.n_predictions,
        weights_file=MODEL_PATH,
        params_file=PARAMS_PATH,
    )
    prediction = [
        {"value": value.item(), "category": category} for value, category in prediction
    ]
    return {"prediction": prediction}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
