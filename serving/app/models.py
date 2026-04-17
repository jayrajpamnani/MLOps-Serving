from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── /classify ────────────────────────────────────────────────────────────────

class ClassifyRequest(BaseModel):
    account: str = Field(..., description="User / account ID")
    date: str = Field(..., description="Transaction date YYYY-MM-DD")
    amount: int = Field(..., description="Amount in cents (negative = expense)")
    payee_name: str = Field(..., description="Raw payee / merchant string")
    imported_id: str = Field("", description="External transaction identifier")


class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    source: str = Field(description="'layer1' or 'layer2'")
    model_version: str


# ── /feedback ────────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    transaction_id: str
    user_id: str
    payee: str
    amount: int
    date: str
    original_prediction: Optional[str] = None
    original_confidence: Optional[float] = None
    source: str = "layer1"
    final_label: str
    reviewed_by_user: bool
    timestamp: Optional[str] = None


class FeedbackRow(BaseModel):
    id: int
    transaction_id: str
    user_id: str
    payee: str
    amount: int
    date: str
    original_prediction: Optional[str]
    original_confidence: Optional[float]
    source: str
    final_label: str
    reviewed_by_user: bool
    timestamp: str


# ── /tag-example ─────────────────────────────────────────────────────────────

class TagExampleRequest(BaseModel):
    user_id: str
    payee: str
    custom_category: str


class TagExampleResponse(BaseModel):
    status: str = "ok"
    id: int


# ── /custom-categories ───────────────────────────────────────────────────────

class CustomCategoriesResponse(BaseModel):
    categories: list[str]


# ── /suggestion-response ─────────────────────────────────────────────────────

class SuggestionAction(str, Enum):
    accept = "accept"
    dismiss = "dismiss"


class SuggestionResponseRequest(BaseModel):
    user_id: str
    transaction_id: str
    action: SuggestionAction
    suggested_category: str


# ── /health ──────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    model_version: str
    uptime_seconds: float


# ── generic ──────────────────────────────────────────────────────────────────

class StatusResponse(BaseModel):
    status: str = "ok"
