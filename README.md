# 🚲 Dublin Bikes

A full-stack web application for exploring Dublin Bikes stations, checking real-time availability, planning routes, and predicting future bike availability using a machine learning model.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Running the Scraper](#running-the-scraper)
  - [Generating the ML Model](#generating-the-ml-model)
- [ML Prediction API](#ml-prediction-api)
- [Team](#team)

---

## Features

- **Interactive Map**: View all Dublin Bikes stations on a Leaflet map with live availability data.
- **Station Detail**: See historical availability, hourly forecasts, and daily averages for any station.
- **Weather Integration**: Current conditions and forecasts displayed alongside bike data.
- **Route Planning**: Get directions between two points with bike-aware routing (via ORS/Google).
- **User Accounts**: Register, log in, set a profile avatar, and save favourite stations.
- **ML Availability Prediction**: Predict the number of available bikes at a station for a given time and weather conditions (MAE 1.67 bikes, R2 0.92).

---

## Architecture

| Layer    | Technology                                                        |
| -------- | ----------------------------------------------------------------- |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS, Leaflet, Recharts |
| Backend  | Flask, SQLAlchemy, APScheduler                                    |
| Database | MySQL                                                             |
| ML       | scikit-learn (trained in Jupyter notebooks)                       |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL server

### Environment Variables

The app reads secrets from a `.env` file in the `backend/` directory. Copy `backend/env.txt` as a starting point:

```bash
cp backend/env.txt backend/.env
```

Then fill in your values:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_PORT=3306
DB_NAME=local_databasejcdecaux
DB_URI=127.0.0.1

BIKE_API_KEY=your_jcdecaux_api_key
GOOGLE_KEY=your_google_maps_api_key
ORS_KEY=your_openrouteservice_api_key

FLASK_SECRET_KEY=a_random_secret_string
```

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/HazelY90/COMP30830SE.git
   cd COMP30830SE
   ```

2. Create and activate a virtual environment:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:

   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`.

### Frontend Setup

1. Install Node dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`.

### Running the Scraper

The scraper continuously fetches live station data from the JCDecaux API and writes it to the database.

```bash
cd backend
python scraper/scraper.py
```

Make sure your `BIKE_API_KEY` is set in `.env` before running.

### Generating the ML Model

The trained model (`bike_availability_model.pkl`, ~357 MB) is not included in the repository. Generate it locally using the notebooks in `other/`:

1. Open and run `other/FeatureEngineering(MergedData).ipynb` top to bottom — this produces `other/engineered_data.csv`.
2. Open and run `other/ModelTraining.ipynb` top to bottom — this trains the model and saves it to `backend/models/bike_availability_model.pkl`.

The backend will fail to start without this file, so generate it before running `app.py`.

---

## ML Prediction API

**Endpoint:** `GET /api/station/<station_id>/hourly-forecast`

The model predicts `num_bikes_available` for a given station, hour, day, and weather conditions.

| Parameter     | Type  | Description                 | Example |
| ------------- | ----- | --------------------------- | ------- |
| `station_id`  | int   | Dublin Bikes station number | `10`    |
| `hour`        | int   | Hour of day (0–23)          | `9`     |
| `day`         | int   | Day of month (1–31)         | `15`    |
| `day_of_week` | int   | 0=Mon … 6=Sun               | `2`     |
| `temperature` | float | Air temperature in °C       | `8.5`   |
| `rainy`       | int   | 0 = dry, 1 = raining        | `0`     |



**Performance:** MAE 1.67 bikes · R2 0.92

