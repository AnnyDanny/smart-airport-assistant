
# Smart Airport Assistant (CPH)

An intelligent, data-driven decision-support application that combines live flight schedules, real-time weather forecasts, and historical machine learning models to help travelers determine optimal airport arrival times for Copenhagen Airport (CPH).

---

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

## Application and Architecture

* **Backend Engine:** Built using **FastAPI** to deliver RESTful endpoints, async data fetching, and automated Swagger/OpenAPI documentation.
* **Automated Testing:** Extensive test suites implemented with **Pytest** covering data processing routines, inference logic, caching fallbacks, and REST endpoints.
* **Cloud Hosting:** API backend deployed on **Render**; static web frontend hosted on **Vercel**.

---

## Project Setup and Local Development Guide

### Prerequisites

Ensure you have the following installed on your machine:
* **Python:** `3.10` or higher
* **Git:** For cloning the repository
* **API Keys Required:**
  * [AviationStack API Key](https://aviationstack.com/) (Live flight data)
---

## Step-by-Step Installation
### Step 1: Clone the Repository
### Step 2: Set Up Virtual Environment
##### On macOS / Linux:
python3 -m venv venv
source venv/bin/activate
##### On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
### Step 3: Install Dependencies:
pip install --upgrade pip
pip install -r requirements.txt


### Repository Structure

```
├── backend/                             # Core Python backend application and API logic
│   ├── api.py                           # FastAPI application entry point and REST endpoint definitions
│   ├── collect_data.py                  # Fetches live flight statuses from the AviationStack API with local caching
│   ├── live_preprocessing.py            # Formats real-time payloads, encodes categories, and prepares matrices for inference
│   ├── recommendation_engine.py         # Loads the remote ML model and calculates final passenger arrival recommendations
│   └── weather_service.py               # Connects to the Open-Meteo API to retrieve real-time weather conditions for CPH
├── data/                                # Data storage directory for historical records and API caches
│   ├── live/                            # Local JSON cache files for live flight and weather responses to prevent API rate limiting
│   └── raw/                             # Original Kaggle historical flight dataset used for model training
├── frontend/                            # Client-side user interface files
│   ├── index.html                       # HTML structure for the passenger search dashboard and recommendation display
│   ├── script.js                        # Client-side JavaScript handling form input, backend API calls, and UI rendering
│   └── style.css                        # Styling and layout rules for responsive web display
├── machine-learning/                    # Data science workflows, Jupyter notebooks, and model training scripts
│   ├── 01_data_exploration.ipynb        # Exploratory Data Analysis on raw historical flight datasets
│   ├── 02_preprocessing.ipynb           # Notebook for testing feature engineering and missing value strategies
│   ├── 03_model_training.ipynb          # Notebook for training, evaluating, and serializing the Random Forest classifier
│   └── preprocessing.py                 # Pipeline functions for feature creation, selection, and encoding
├── .gitignore                           # Specifies untracked files and folders to ignore
├── LICENSE                              # Open-source license terms for the project repository
├── README.md                            # Comprehensive project documentation, setup guides, and system architecture
├── package-lock.json                    # Locks the exact version of Prettier for consistent code formatting
├── package.json                         # Configuration file specifying Prettier for code formatting
├── requirements.txt                     # List of Python dependencies required for the backend
```

### Using the Web Interface

1. **Enter Flight Details:**
   * Open the application in any web browser: https://smart-airport-assistant.vercel.app/
   * Enter your flight number (e.g., `SK1420`) and select your travel date.
   * Click **"Search" button**.

2. **View Live Results and Decision Support:**
   * **Delay Probability Score:** Displays a calculated risk percentage (e.g., *Delay risk: High*) generated by the Random Forest model based on historical airline and schedule patterns.
   * **Live Updates:** Displays real-time airport status from AviationStack and current weather conditions at Copenhagen Airport (CPH) via Open-Meteo.
   * **Smart Arrival Recommendation:** Outputs a clear, actionable instruction (e.g., *"Recommended: Arrive earlier during busy periods."*).
