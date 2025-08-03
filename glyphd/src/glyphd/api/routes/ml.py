from fastapi import APIRouter, HTTPException
from starlette import status

from glyphd.api.models.ml import MLPredictionRequest, MLPredictionResponse
from glyphsieve.ml.predictor import predict_is_gpu

router = APIRouter(tags=["ML"])


@router.post(
    "/ml/is-gpu",
    response_model=MLPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="GPU Classification Prediction",
    description="Classify whether a listing title represents an NVIDIA GPU using ML model",
)
async def predict_gpu_classification(request: MLPredictionRequest) -> MLPredictionResponse:
    """
    Predict if a listing is an NVIDIA GPU based on the title.

    Uses the trained ML classifier to predict whether the given title
    represents an NVIDIA GPU listing.

    Args:
        request: Request containing the title to classify

    Returns:
        MLPredictionResponse: Prediction result with boolean classification and confidence score

    Raises:
        HTTPException: If there's an error during prediction
    """
    try:
        # Use the existing predictor function
        # Pass empty string for bulk_notes since endpoint only accepts title
        is_gpu, score = predict_is_gpu(request.title, "")

        return MLPredictionResponse(ml_is_gpu=is_gpu, ml_score=score)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error during GPU prediction: {e!s}"
        )
