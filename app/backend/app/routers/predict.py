from typing import AsyncGenerator

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from app.schemas.classify import ClassifyRequest, ClassifyResponse
from app.services.classifier import Classifier

router = APIRouter(prefix="/predict", tags=["Predict"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ClassifyResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "label": "positive",
                        "score": 0.98
                    }
                }
            },
        }
    },
)
async def prediction_sentiment(classify_request: ClassifyRequest, request: Request):
    print("Processing classify request:", classify_request.text)
    text_classifier: Classifier = request.app.state.text_classifier
    output = text_classifier.get_sentiment_label_and_score(classify_request.text)
    return JSONResponse(content=output)
