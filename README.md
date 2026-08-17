
# Smart Airport Assistant (CPH)

An intelligent, data-driven decision-support application that combines live flight schedules, real-time weather forecasts, and historical machine learning models to help travelers determine optimal airport arrival times for Copenhagen Airport (CPH).

---

The main goal of the Smart Airport Assistant is to improve the travel experience for airline passengers by helping them deal with flight delays and airport crowding using data. Usually, airlines inform travelers about delays after they are already at the airport, which causes long waiting times and stress. This project helps solve that problem by giving passengers clear, personalized advice on when to leave for the airport before they set off.

To achieve this, the project combines machine learning with real-time data. The application uses a trained Random Forest model together with live information from the AviationStack and Open-Meteo APIs. This allows the system to analyze past flight delays, current flight schedules, and weather conditions at Copenhagen Airport. Rather than showing complicated data or statistics, the system turns delay risks and weather warnings into simple, practical advice - such as telling the user to arrive earlier when the delay risk is high.

In addition to the technical setup, the project relies heavily on user experience research and reflective analysis. Based on a Design Thinking approach, user interviews at Copenhagen Airport showed that passengers do not just want raw data; they need clear, reassuring guidance that is easy to understand. Furthermore, the analysis of the project proved that machine learning and live data must work together. Machine learning identifies long-term delay patterns, while live APIs capture sudden weather changes. By combining these two sources into a simple web application, the project shows how machine learning and good design can help solve everyday travel problems.

---
<img width="2000" height="2000" alt="Green Simple Company Negative Aircraft Space Logo" src="https://github.com/user-attachments/assets/b6edf34a-68f2-4577-844d-7cb515fb8d45" />

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
### Step 4: Configure Environment Variables
Create a `.env` file in the `backend/` directory by copying the `.env.example` file:
```cp .env.example backend/.env```
Open the new .env file in your editor and insert your personal AviationStack API key:
```AVIATIONSTACK_API_KEY=your_actual_api_key_here```
### Step 5: Start the Backend Server
Navigate to the backend/ directory and launch the FastAPI server using Uvicorn:
```cd backend```
```uvicorn api:app --reload --port 8000```
Local API Base URL: ```http://127.0.0.1:8000/```
API Documentation: ```http://127.0.0.1:8000/docs```
### Step 6: Launch the Web Frontend
Open a new terminal windows and navigate to the directory /frontend:
```cd frontend```
```python3 -m http.server 3000```, then
open http://localhost:3000 in your web browser

---

### Repository Structure

```
├── backend/                             # Core Python backend application and API logic
│   ├── api.py                           # FastAPI application entry point and REST endpoint definitions
│   ├── collect_data.py                  # Fetches live flight statuses from the AviationStack API with local caching
│   ├── config.py                        # Loads environment variables and secures the AviationStack API key
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

---
### Using the Web Interface

1. **Enter Flight Details:**
   * Open the application in any web browser: https://smart-airport-assistant.vercel.app/
   * Enter your flight number (e.g., `AM7815`)
   * Click **"Search" button**.

2. **View Live Results and Decision Support:**
   * **Delay Probability Score:** Displays a calculated risk percentage (e.g., *Delay risk: High*) generated by the Random Forest model based on historical airline and schedule patterns.
   * **Live Updates:** Displays real-time airport status from AviationStack and current weather conditions at Copenhagen Airport (CPH) via Open-Meteo.
   * **Smart Arrival Recommendation:** Outputs a clear, actionable instruction (e.g., *"Recommended: Arrive earlier during busy periods."*).
  
 
---

### Future Improvements
1. Adding Live Airport Security Data
Security Wait Times: Connect to real-time security line and baggage drop wait time data at Copenhagen Airport to make arrival recommendations even more accurate.
Instant Alerts: Send notifications to users about sudden gate changes, boarding updates, or last-minute flight delays.
2. Improving the Machine Learning Model
Better Algorithms: Upgrade the model from Random Forest to advanced algorithms like XGBoost to better handle seasonal delay patterns.
Plane Tracking: Track incoming aircraft tail numbers to predict "inbound delays," which happen when a plane arrives late from its previous destination.
Automatic Retraining: Set up an automatic system to retrain the model regularly using fresh flight data to keep predictions accurate over time.
3. Enhancing User Experience and Personalization
Personalized Profiles: Let users input personal travel details.
Expanding to Other Airports: Broaden the app beyond Copenhagen Airport (CPH) to support major European hubs.
In-Terminal Directions: Add indoor airport maps and estimated walking times to gates to help passengers navigate the terminal smoothly.

---

### Resources and Dependencies
* Python Libraries & Core Tools
* Data Processing: pandas, numpy, datetime, pathlib
* Machine Learning: scikit-learn (RandomForestClassifier, LabelEncoder, metrics), joblib, huggingface_hub
* Backend & API: fastapi, uvicorn, pydantic, requests
* Testing & Infrastructure: pytest, git, github-actions
* External APIs & Hosting Services
* AviationStack API – Live Flight Tracking Data
* Open-Meteo API – Weather Forecast Data
* Hugging Face Hub – Remote Machine Learning Model Storage
* Render – Cloud API Backend Deployment
* Vercel – Frontend Web Hosting


* Aviation stack API Documentation: https://docs.apilayer.com/aviationstack/docs/api-documentation
* AviationStack: https://aviationstack.com/
* Weather Data API: https://open-meteo.com/en/docs
* Historical Dataset: https://www.kaggle.com/code/codecavalier/flights-delays-eda-masterclass-python
* scikit-learn: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
* Pandas: https://pandas.pydata.org/docs/
* Joblib: https://joblib.readthedocs.io
* FastAPI: https://fastapi.tiangolo.com
* Pytest: https://docs.pytest.org
* Hugging Face Hub: https://huggingface.co/docs
* Render: https://render.com/docs
* Vercel: https://vercel.com/docs
* EUROCONTROL – Central Office for Delay Analysis (CODA): https://ansperformance.eu
* IATA (International Air Transport Association) – Global Passenger Survey (GPS): https://www.iata.org/
* U.S. Bureau of Transportation Statistics (BTS) – Flight Delays and Causes: https://www.bts.gov/

