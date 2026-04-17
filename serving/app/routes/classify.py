"""POST /classify — full classification pipeline."""

import logging
import time

from fastapi import APIRouter

from app import layer1, layer2
from app.feature_computation import compute_features
from app.models import ClassifyRequest, ClassifyResponse
from app.routes.monitoring import record_request

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse)
async def classify_transaction(req: ClassifyRequest) -> ClassifyResponse:
    t0 = time.perf_counter()

    features = compute_features(req.payee_name, req.amount, req.date)
    feature_vector = features["feature_vector"]

    l1_category, l1_confidence = layer1.predict(feature_vector)

    l2_result = await layer2.classify(req.account, req.payee_name)
    if l2_result is not None:
        category, similarity = l2_result
        record_request(time.perf_counter() - t0, similarity)
        return ClassifyResponse(
            category=category,
            confidence=round(similarity, 4),
            source="layer2",
            model_version=layer1.get_model_version(),
        )

    record_request(time.perf_counter() - t0, l1_confidence)
    return ClassifyResponse(
        category=l1_category,
        confidence=round(l1_confidence, 4),
        source="layer1",
        model_version=layer1.get_model_version(),
    )
