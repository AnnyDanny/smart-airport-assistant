## Data

The project leverages both static historical data for model training and live APIs for real-time inference:

* **Historical Flight Records:** Kaggle-sourced historical flight dataset utilized for data cleaning, feature engineering, and model training (identifying delay trends across airlines, flight numbers, and schedules).
* **Live Flight Statuses:** Integrated via the **AviationStack REST API** to retrieve live gate, terminal, and departure information.
* **Environmental Data:** Integrated via the **Open-Meteo REST API** to capture real-time weather conditions impacting flight schedules.
* **API Resiliency:** Built-in local JSON caching mechanisms handle third-party API rate limits and fallbacks to ensure zero downtime.

---

## Machine Learning

The predictive pipeline evaluates historical patterns to calculate delay probabilities:

* **Model Architecture:** Trained using a **Random Forest Classifier** (`scikit-learn`) optimized for tabular classification.
* **Preprocessing Pipeline:** Modularized pipeline (`live_preprocessing.py`, `preprocessing.py`) handling missing values, feature creation, and categorical encoding via `LabelEncoder`.
* **Model Operations (MLOps):** Artifacts serialized using `joblib` and hosted remotely on **Hugging Face Hub** to optimize repository size and enable lightweight backend loading on server startup.
* **Evaluation Metrics:** Evaluated using `accuracy_score`, `confusion_matrix`, and `classification_report`.

---
