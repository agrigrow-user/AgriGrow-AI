from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from core import (
    APP_NAME,
    FEATURES,
    FEATURE_LABELS,
    build_model_registry,
    compute_crop_stats,
    compute_sensitivity,
    compute_validation_ranges,
    crop_tip,
    evaluate_models,
    explain_features,
    load_dataset,
    load_models_if_available,
)
from weather import fetch_weather, search_locations


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"


class CropRequest(BaseModel):
    N: float = Field(..., ge=0, le=300)
    P: float = Field(..., ge=0, le=300)
    K: float = Field(..., ge=0, le=300)
    temperature: float = Field(..., ge=-10, le=60)
    humidity: float = Field(..., ge=0, le=100)
    ph: float = Field(..., ge=0, le=14)
    rainfall: float = Field(..., ge=0, le=1000)
    model_name: str | None = None


@dataclass(frozen=True)
class WebRuntime:
    models: dict
    accuracies: dict
    stats: dict
    validation_ranges: dict
    crop_count: int
    sample_count: int
    trained_in_memory: bool


app = FastAPI(
    title="Weather-Aware Crops Recommendation API",
    version="1.0.0",
    description="FastAPI deployment wrapper for AgriYieldAI crop recommendations.",
)


def train_models_in_memory(df):
    registry = build_model_registry()
    X = df[FEATURES].to_numpy(dtype=float)
    y = df["label"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {}
    accuracies = {}
    for name, (_, model) in registry.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        models[name] = model
        accuracies[name] = float(accuracy_score(y_test, predictions))
    return models, accuracies


@lru_cache(maxsize=1)
def get_runtime() -> WebRuntime:
    df = load_dataset()
    stats = compute_crop_stats(df)
    validation_ranges = compute_validation_ranges(df)
    models, accuracies = load_models_if_available()
    trained_in_memory = False

    if models is None:
        models, accuracies = train_models_in_memory(df)
        trained_in_memory = True
    elif not accuracies:
        accuracies = evaluate_models(models, df)

    return WebRuntime(
        models=models,
        accuracies=accuracies or {},
        stats=stats,
        validation_ranges=validation_ranges,
        crop_count=int(df["label"].nunique()),
        sample_count=int(len(df)),
        trained_in_memory=trained_in_memory,
    )


def request_values(payload: CropRequest) -> dict:
    data = payload.model_dump()
    return {feature: float(data[feature]) for feature in FEATURES}


def confidence_note(confidence: float, alternatives: list[dict]) -> str:
    if not alternatives:
        return "Confidence available for the recommended crop."

    top2 = float(alternatives[0]["confidence"])
    gap = max(confidence - top2, 0.0)
    if confidence < 0.45 or gap < 0.10:
        return f"Low confidence: similar crops compete with a {gap * 100:.1f}% top gap."
    if confidence < 0.70:
        return f"Moderate confidence with a {gap * 100:.1f}% top gap."
    return "High confidence recommendation."


def range_warnings(values: dict, validation_ranges: dict) -> list[str]:
    warnings = []
    for feature, value in values.items():
        ranges = validation_ranges[feature]
        label = FEATURE_LABELS.get(feature, feature)
        if value < ranges["data_min"] or value > ranges["data_max"]:
            warnings.append(
                f"{label} is outside the training data range "
                f"({ranges['data_min']:.1f}-{ranges['data_max']:.1f})."
            )
    return warnings


def public_file(name: str) -> FileResponse:
    path = PUBLIC_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


@app.get("/", include_in_schema=False)
def home():
    return public_file("index.html")


@app.get("/styles.css", include_in_schema=False)
def styles():
    return public_file("styles.css")


@app.get("/app.js", include_in_schema=False)
def script():
    return public_file("app.js")


@app.get("/agri-hero.png", include_in_schema=False)
def hero_image():
    return public_file("agri-hero.png")


@app.get("/api/health")
def health():
    runtime = get_runtime()
    return {
        "status": "ok",
        "service": APP_NAME,
        "models": list(runtime.models.keys()),
        "trained_in_memory": runtime.trained_in_memory,
    }


@app.get("/api/metadata")
def metadata():
    runtime = get_runtime()
    return {
        "features": [
            {
                "key": feature,
                "label": FEATURE_LABELS.get(feature, feature),
                "range": runtime.validation_ranges[feature],
            }
            for feature in FEATURES
        ],
        "models": [
            {"name": name, "accuracy": float(runtime.accuracies.get(name, 0.0))}
            for name in runtime.models.keys()
        ],
        "crop_count": runtime.crop_count,
        "sample_count": runtime.sample_count,
    }


@app.post("/api/predict")
def predict(payload: CropRequest):
    runtime = get_runtime()
    values = request_values(payload)
    model_name = payload.model_name or next(iter(runtime.models.keys()))

    if model_name not in runtime.models:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model_name}")

    model = runtime.models[model_name]
    X = np.array([[values[feature] for feature in FEATURES]])
    probabilities = model.predict_proba(X)[0]
    classes = model.classes_
    top_indexes = list(reversed(probabilities.argsort()))

    top_crop = str(classes[top_indexes[0]])
    confidence = float(probabilities[top_indexes[0]])
    alternatives = [
        {"crop": str(classes[index]), "confidence": float(probabilities[index])}
        for index in top_indexes[1:4]
    ]

    sensitivity = [
        {
            "feature": FEATURE_LABELS.get(item["feature"], item["feature"]),
            "delta_up": float(item["delta_up"]),
            "delta_down": float(item["delta_down"]),
        }
        for item in compute_sensitivity(model, values, top_crop, runtime.validation_ranges)[:5]
    ]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "accuracy": float(runtime.accuracies.get(model_name, 0.0)),
        "inputs": values,
        "crop": top_crop,
        "confidence": confidence,
        "alternatives": alternatives,
        "explanations": explain_features(top_crop, values, runtime.stats),
        "tip": crop_tip(top_crop),
        "sensitivity": sensitivity,
        "confidence_note": confidence_note(confidence, alternatives),
        "warnings": range_warnings(values, runtime.validation_ranges),
    }


@app.get("/api/weather")
def weather(city: str = Query(..., min_length=2)):
    try:
        return fetch_weather(city.strip())
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/locations")
def locations(q: str = Query(..., min_length=2), limit: int = Query(5, ge=1, le=10)):
    try:
        return {"locations": search_locations(q.strip(), limit=limit)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
