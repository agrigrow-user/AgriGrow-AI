# Execute this statement.
# Import csv.
import csv
# Import json.
import json
# Import logging.
import logging
# Import datetime from datetime.
from datetime import datetime
# Import Path from pathlib.
from pathlib import Path

# Import joblib.
import joblib
# Import numpy as np.
import numpy as np
# Import pandas as pd.
import pandas as pd
# Import RandomForestClassifier from sklearn.ensemble.
from sklearn.ensemble import RandomForestClassifier
# Import LogisticRegression from sklearn.linear_model.
from sklearn.linear_model import LogisticRegression
# Import accuracy_score from sklearn.metrics.
from sklearn.metrics import accuracy_score
# Import train_test_split from sklearn.model_selection.
from sklearn.model_selection import train_test_split
# Import Pipeline from sklearn.pipeline.
from sklearn.pipeline import Pipeline
# Import StandardScaler from sklearn.preprocessing.
from sklearn.preprocessing import StandardScaler
# Import SVC from sklearn.svm.
from sklearn.svm import SVC
# Import DecisionTreeClassifier from sklearn.tree.
from sklearn.tree import DecisionTreeClassifier

# Import base_dir, resource_path from paths.
from paths import base_dir, resource_path

# Set APP_NAME.
APP_NAME = 'AgriYieldAI'

# Set FEATURES.
FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
# Set FEATURE_LABELS.
FEATURE_LABELS = {
    # Execute this statement.
    'N': 'Nitrogen (N)',
    # Execute this statement.
    'P': 'Phosphorus (P)',
    # Execute this statement.
    'K': 'Potassium (K)',
    # Execute this statement.
    'temperature': 'Temperature (C)',
    # Execute this statement.
    'humidity': 'Humidity (%)',
    # Execute this statement.
    'ph': 'pH Level',
    # Execute this statement.
    'rainfall': 'Rainfall (mm)'
# Close the previous block or structure.
}

# Set DOMAIN_LIMITS.
DOMAIN_LIMITS = {
    # Execute this statement.
    'N': (0.0, 300.0),
    # Execute this statement.
    'P': (0.0, 300.0),
    # Execute this statement.
    'K': (0.0, 300.0),
    # Execute this statement.
    'temperature': (-10.0, 60.0),
    # Execute this statement.
    'humidity': (0.0, 100.0),
    # Execute this statement.
    'ph': (0.0, 14.0),
    # Execute this statement.
    'rainfall': (0.0, 1000.0)
# Close the previous block or structure.
}

# Set BASE_DIR.
BASE_DIR = base_dir()
# Set DATA_PATH.
DATA_PATH = resource_path('Crop_recommendation.csv')
# Set MODEL_META_PATH.
MODEL_META_PATH = BASE_DIR / 'crop_model_meta.json'
# Set HISTORY_PATH.
HISTORY_PATH = BASE_DIR / 'prediction_history.csv'

# Set HISTORY_FIELDS.
HISTORY_FIELDS = ['timestamp', 'model', 'crop', 'confidence'] + FEATURES

# Set LOGGER.
LOGGER = logging.getLogger(APP_NAME)

# Define function model_path.
def model_path(key: str) -> Path:
    # Return the computed value.
    return BASE_DIR / f'crop_model_{key}.joblib'


# Define function build_model_registry.
def build_model_registry():
    # Return the computed value.
    return {
        # Set 'Random Forest': ('rf', RandomForestClassifier(n_estimators.
        'Random Forest': ('rf', RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)),
        # Multi-model options are kept for later use but are commented out for now.
        # 'Decision Tree': ('dt', DecisionTreeClassifier(random_state=42, max_depth=None)),
        # 'SVM (RBF)': (
        #     'svm',
        #     Pipeline([
        #         ('scaler', StandardScaler()),
        #         ('svc', SVC(kernel='rbf', probability=True, gamma='scale', random_state=42))
        #     ])
        # ),
        # 'Logistic Regression': (
        #     'logreg',
        #     Pipeline([
        #         ('scaler', StandardScaler()),
        #         ('logreg', LogisticRegression(max_iter=2000))
        #     ])
        # )
    # Close the previous block or structure.
    }


# Define function load_dataset.
def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    # Set df.
    df = pd.read_csv(path)
    # Set missing.
    missing = [c for c in FEATURES + ['label'] if c not in df.columns]
    # Check condition and run block if true.
    if missing:
        # Raise an exception.
        raise ValueError(f'Missing columns in dataset: {missing}')
    # Return the computed value.
    return df


# Define function compute_validation_ranges.
def compute_validation_ranges(df: pd.DataFrame) -> dict:
    # Set ranges.
    ranges = {}
    # Loop over items in a sequence.
    for f in FEATURES:
        # Set data_min.
        data_min = float(df[f].min())
        # Set data_max.
        data_max = float(df[f].max())
        # Set rec_min.
        rec_min = float(df[f].quantile(0.05))
        # Set rec_max.
        rec_max = float(df[f].quantile(0.95))

        # Set dmin, dmax.
        dmin, dmax = DOMAIN_LIMITS.get(f, (None, None))
        # Set hard_min.
        hard_min = dmin if dmin is not None else data_min
        # Set hard_max.
        hard_max = dmax if dmax is not None else data_max
        # Check condition and run block if true.
        if dmin is not None:
            # Set rec_min.
            rec_min = max(rec_min, dmin)
        # Check condition and run block if true.
        if dmax is not None:
            # Set rec_max.
            rec_max = min(rec_max, dmax)

        # Set ranges[f].
        ranges[f] = {
            # Execute this statement.
            'min': hard_min,
            # Execute this statement.
            'max': hard_max,
            # Execute this statement.
            'data_min': data_min,
            # Execute this statement.
            'data_max': data_max,
            # Execute this statement.
            'rec_min': rec_min,
            # Execute this statement.
            'rec_max': rec_max
        # Close the previous block or structure.
        }
    # Return the computed value.
    return ranges


# Define function compute_crop_stats.
def compute_crop_stats(df: pd.DataFrame) -> dict:
    # Set stats.
    stats = {}
    # Loop over items in a sequence.
    for crop, group in df.groupby('label'):
        # Set stats[crop].
        stats[crop] = {}
        # Loop over items in a sequence.
        for f in FEATURES:
            # Set q1.
            q1 = float(group[f].quantile(0.25))
            # Set q2.
            q2 = float(group[f].quantile(0.50))
            # Set q3.
            q3 = float(group[f].quantile(0.75))
            # Set stats[crop][f].
            stats[crop][f] = {'q1': q1, 'q2': q2, 'q3': q3}
    # Return the computed value.
    return stats

# Define function train_and_save_models.
def train_and_save_models(df: pd.DataFrame) -> tuple:
    # Set registry.
    registry = build_model_registry()
    # Set X.
    X = df[FEATURES].to_numpy(dtype=float)
    # Set y.
    y = df['label'].to_numpy()

    # Set X_train, X_test, y_train, y_test.
    X_train, X_test, y_train, y_test = train_test_split(
        # Set X, y, test_size.
        X, y, test_size=0.2, random_state=42, stratify=y
    # Close the previous block or structure.
    )

    # Set models.
    models = {}
    # Set accuracies.
    accuracies = {}

    # Loop over items in a sequence.
    for name, (key, model) in registry.items():
        # Call model.fit.
        model.fit(X_train, y_train)
        # Set preds.
        preds = model.predict(X_test)
        # Set acc.
        acc = accuracy_score(y_test, preds)
        # Set models[name].
        models[name] = model
        # Set accuracies[name].
        accuracies[name] = acc
        # Call joblib.dump.
        joblib.dump(model, model_path(key))

    # Set meta.
    meta = {
        # Execute this statement.
        'features': FEATURES,
        # Execute this statement.
        'accuracy': accuracies,
        # Execute this statement.
        'n_samples': len(df),
        # Execute this statement.
        'trained_at': datetime.now().isoformat()
    # Close the previous block or structure.
    }
    # Open and manage a context/resource.
    with open(MODEL_META_PATH, 'w', encoding='utf-8') as f:
        # Set json.dump(meta, f, indent.
        json.dump(meta, f, indent=2)

    # Return the computed value.
    return models, accuracies


# Define function load_models_if_available.
def load_models_if_available() -> tuple:
    # Set registry.
    registry = build_model_registry()
    # Set models.
    models = {}
    # Set missing.
    missing = False
    # Loop over items in a sequence.
    for name, (key, _) in registry.items():
        # Set path.
        path = model_path(key)
        # Check condition and run block if true.
        if not path.exists():
            # Set missing.
            missing = True
            # Exit the current loop.
            break

    # Check condition and run block if true.
    if missing:
        # Return the computed value.
        return None, None

    # Loop over items in a sequence.
    for name, (key, _) in registry.items():
        # Set models[name].
        models[name] = joblib.load(model_path(key))

    # Set accuracies.
    accuracies = None
    # Check condition and run block if true.
    if MODEL_META_PATH.exists():
        # Open and manage a context/resource.
        with open(MODEL_META_PATH, 'r', encoding='utf-8') as f:
            # Set meta.
            meta = json.load(f)
            # Set accuracies.
            accuracies = meta.get('accuracy')

    # Return the computed value.
    return models, accuracies


# Define function evaluate_models.
def evaluate_models(models: dict, df: pd.DataFrame) -> dict:
    # Set X.
    X = df[FEATURES].to_numpy(dtype=float)
    # Set y.
    y = df['label'].to_numpy()
    # Set X_train, X_test, y_train, y_test.
    X_train, X_test, y_train, y_test = train_test_split(
        # Set X, y, test_size.
        X, y, test_size=0.2, random_state=42, stratify=y
    # Close the previous block or structure.
    )

    # Set accuracies.
    accuracies = {}
    # Loop over items in a sequence.
    for name, model in models.items():
        # Set preds.
        preds = model.predict(X_test)
        # Set accuracies[name].
        accuracies[name] = accuracy_score(y_test, preds)
    # Return the computed value.
    return accuracies


# Define function load_or_train_models.
def load_or_train_models(df: pd.DataFrame) -> tuple:
    # Set models, accuracies.
    models, accuracies = load_models_if_available()
    # Check condition and run block if true.
    if models is None:
        # Call LOGGER.info.
        LOGGER.info('Training models from scratch')
        # Return the computed value.
        return train_and_save_models(df)

    # Check condition and run block if true.
    if not accuracies:
        # Call LOGGER.info.
        LOGGER.info('Evaluating loaded models for accuracy')
        # Set accuracies.
        accuracies = evaluate_models(models, df)
    # Return the computed value.
    return models, accuracies

# Define function score_feature_match.
def score_feature_match(crop: str, values: dict, stats: dict) -> list:
    # Set items.
    items = []
    # Check condition and run block if true.
    if crop not in stats:
        # Return the computed value.
        return items
    # Loop over items in a sequence.
    for f, val in values.items():
        # Set q1.
        q1 = stats[crop][f]['q1']
        # Set q2.
        q2 = stats[crop][f]['q2']
        # Set q3.
        q3 = stats[crop][f]['q3']
        # Execute this statement.
        denom = (q3 - q1) if (q3 - q1) != 0 else 1.0
        # Set score.
        score = abs(val - q2) / denom
        # Call items.append.
        items.append((score, f, val, q1, q3))
    # Set items.sort(key.
    items.sort(key=lambda x: x[0])
    # Return the computed value.
    return items


# Define function explain_features.
def explain_features(crop: str, values: dict, stats: dict, max_items: int = 4) -> list:
    # Set items.
    items = score_feature_match(crop, values, stats)
    # Set explanations.
    explanations = []
    # Loop over items in a sequence.
    for _, f, val, q1, q3 in items[:max_items]:
        # Set label.
        label = FEATURE_LABELS.get(f, f)
        # Check condition and run block if true.
        if q1 <= val <= q3:
            # Call explanations.append.
            explanations.append(f'{label} is within typical range ({q1:.1f}-{q3:.1f}).')
        # Check an alternative condition.
        elif val < q1:
            # Call explanations.append.
            explanations.append(f'{label} is below typical range ({q1:.1f}-{q3:.1f}).')
        # Fallback branch when conditions do not match.
        else:
            # Call explanations.append.
            explanations.append(f'{label} is above typical range ({q1:.1f}-{q3:.1f}).')
    # Return the computed value.
    return explanations


# Define function crop_tip.
def crop_tip(crop: str) -> str:
    # Set tips.
    tips = {
        # Execute this statement.
        'rice': 'Maintain steady moisture and avoid long dry periods for best results.',
        # Execute this statement.
        'maize': 'Good drainage helps maize avoid root stress after heavy rain.',
        # Execute this statement.
        'wheat': 'Stable temperatures and moderate rainfall improve grain quality.',
        # Execute this statement.
        'cotton': 'Warm conditions and balanced nitrogen support healthy boll growth.',
        # Execute this statement.
        'banana': 'High humidity and consistent irrigation improve fruit size.'
    # Close the previous block or structure.
    }
    # Return the computed value.
    return tips.get(crop, 'Monitor soil moisture and adjust irrigation based on weather trends.')


# Define function compute_sensitivity.
def compute_sensitivity(model, values: dict, target_crop: str, ranges: dict) -> list:
    # Set base_x.
    base_x = np.array([[values[f] for f in FEATURES]])
    # Set proba.
    proba = model.predict_proba(base_x)[0]
    # Set classes.
    classes = model.classes_
    # Check condition and run block if true.
    if target_crop not in classes:
        # Return the computed value.
        return []
    # Set idx.
    idx = list(classes).index(target_crop)
    # Set base_score.
    base_score = float(proba[idx])

    # Set results.
    results = []
    # Loop over items in a sequence.
    for f in FEATURES:
        # Set r.
        r = ranges[f]
        # Set span.
        span = r['max'] - r['min']
        # Set delta.
        delta = span * 0.1 if span > 0 else max(0.01, abs(values[f]) * 0.05)

        # Set up_val.
        up_val = min(r['max'], values[f] + delta)
        # Set down_val.
        down_val = max(r['min'], values[f] - delta)

        # Set up_values.
        up_values = values.copy()
        # Set up_values[f].
        up_values[f] = up_val
        # Set down_values.
        down_values = values.copy()
        # Set down_values[f].
        down_values[f] = down_val

        # Set up_x.
        up_x = np.array([[up_values[x] for x in FEATURES]])
        # Set down_x.
        down_x = np.array([[down_values[x] for x in FEATURES]])

        # Set up_score.
        up_score = float(model.predict_proba(up_x)[0][idx])
        # Set down_score.
        down_score = float(model.predict_proba(down_x)[0][idx])

        # Call results.append.
        results.append({
            # Execute this statement.
            'feature': f,
            # Execute this statement.
            'delta_up': up_score - base_score,
            # Execute this statement.
            'delta_down': down_score - base_score
        # Execute this statement.
        })

    # Set results.sort(key.
    results.sort(key=lambda x: max(abs(x['delta_up']), abs(x['delta_down'])), reverse=True)
    # Return the computed value.
    return results


# Define function append_history.
def append_history(result: dict):
    # Set row.
    row = {
        # Execute this statement.
        'timestamp': result['timestamp'].isoformat(),
        # Execute this statement.
        'model': result['model'],
        # Execute this statement.
        'crop': result['top1'],
        # Execute this statement.
        'confidence': f"{result['confidence']:.6f}"
    # Close the previous block or structure.
    }
    # Loop over items in a sequence.
    for f in FEATURES:
        # Set row[f].
        row[f] = f"{result['inputs'][f]:.4f}"

    # Set file_exists.
    file_exists = HISTORY_PATH.exists()
    # Open and manage a context/resource.
    with open(HISTORY_PATH, 'a', newline='', encoding='utf-8') as f:
        # Set writer.
        writer = csv.DictWriter(f, fieldnames=HISTORY_FIELDS)
        # Check condition and run block if true.
        if not file_exists:
            # Call writer.writeheader.
            writer.writeheader()
        # Call writer.writerow.
        writer.writerow(row)


# Define function load_history.
def load_history() -> list:
    # Check condition and run block if true.
    if not HISTORY_PATH.exists():
        # Return the computed value.
        return []
    # Set items.
    items = []
    # Open and manage a context/resource.
    with open(HISTORY_PATH, 'r', newline='', encoding='utf-8') as f:
        # Set reader.
        reader = csv.DictReader(f)
        # Loop over items in a sequence.
        for row in reader:
            # Start a protected block for error handling.
            try:
                # Set timestamp.
                timestamp = datetime.fromisoformat(row['timestamp'])
                # Set inputs.
                inputs = {f: float(row.get(f, 0.0)) for f in FEATURES}
                # Call items.append.
                items.append({
                    # Execute this statement.
                    'timestamp': timestamp,
                    # Execute this statement.
                    'model': row.get('model', 'Unknown'),
                    # Execute this statement.
                    'top1': row.get('crop', '-'),
                    # Execute this statement.
                    'confidence': float(row.get('confidence', 0.0)),
                    # Execute this statement.
                    'inputs': inputs,
                    # Execute this statement.
                    'alternatives': [],
                    # Execute this statement.
                    'explanations': [],
                    # Execute this statement.
                    'tip': '',
                    # Execute this statement.
                    'sensitivity': []
                # Execute this statement.
                })
            # Handle an error case.
            except Exception:
                # Skip to the next loop iteration.
                continue
    # Return the computed value.
    return items
