import logging
from dataclasses import dataclass, field
from pathlib import Path

from core import (
    APP_NAME,
    compute_crop_stats,
    compute_validation_ranges,
    load_dataset,
    load_history,
    load_or_train_models,
)
from gui import CropApp
from paths import base_dir


@dataclass
class AppState:
    models: dict
    accuracies: dict
    stats: dict
    validation_ranges: dict
    best_accuracy: float | None
    active_model_name: str
    current_location: str | None = None
    current_location_display: str | None = None
    history: list = field(default_factory=list)

    def active_model(self):
        return self.models[self.active_model_name]


def setup_logging() -> logging.Logger:
    log_path = Path(base_dir()) / "app.log"
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def main():
    logger = setup_logging()
    logger.info("Starting desktop application")

    try:
        df = load_dataset()
        validation_ranges = compute_validation_ranges(df)
        stats = compute_crop_stats(df)
        models, accuracies = load_or_train_models(df)
        best_accuracy = max(accuracies.values()) if accuracies else None
        active_name = list(models.keys())[0]
        state = AppState(
            models=models,
            accuracies=accuracies or {},
            stats=stats,
            validation_ranges=validation_ranges,
            best_accuracy=best_accuracy,
            active_model_name=active_name,
            history=load_history(),
        )
    except Exception as exc:
        logger.error("Startup error: %s", exc)
        raise

    app = CropApp(state)
    app.mainloop()


if __name__ == "__main__":
    main()
