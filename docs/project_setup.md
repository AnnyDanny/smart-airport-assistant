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
