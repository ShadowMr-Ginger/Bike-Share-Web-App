"""
Production entry point for Windows Server (or any platform).

Features:
  - Waitress WSGI server (cross-platform, no Gunicorn needed)
  - Built-in APScheduler for periodic data scraping (replaces Linux cron)
  - Runs initial scrape on startup to avoid cold-start empty data

Usage:
    cd backend
    pip install -r requirements.txt
    python run.py

Environment variables (.env):
    PORT   - Server port (default: 5000)
    HOST   - Server host (default: 0.0.0.0)
"""

import os
import sys

# Ensure backend root is on path so internal imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from waitress import serve
from apscheduler.schedulers.background import BackgroundScheduler

# Load .env before importing app/scraper (they rely on env vars)
load_dotenv()

from app import app
from scraper.autoscraping import auto_scraping
import scraper.scraper as sc
import database.db_manager as db


def run_initial_scrape():
    """Scrape once on startup so the DB isn't empty."""
    print("[Startup] Running initial scraping...")
    try:
        auto_scraping()
        print("[Startup] Initial scraping completed.")
    except Exception as e:
        print(f"[Startup] Initial scraping failed (non-fatal): {e}")

    # Always fetch daily forecast on startup (independent of the 00:00-00:09 window)
    print("[Startup] Fetching daily forecast...")
    try:
        forecast_daily = sc.get_daily_weather()
        if forecast_daily:
            db.write_to_db_forecast_daily(forecast_daily)
            print("[Startup] Daily forecast loaded.")
        else:
            print("[Startup] Daily forecast empty (API may have no data).")
    except Exception as e:
        print(f"[Startup] Daily forecast fetch failed (non-fatal): {e}")


def start_scheduler():
    """Start APScheduler to mimic Linux cron on Windows."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        auto_scraping,
        "interval",
        minutes=5,
        id="bike_scraper",
        replace_existing=True,
    )
    scheduler.start()
    print("[Scheduler] APScheduler started – scraping every 5 minutes.")


if __name__ == "__main__":
    # 1. Initial scrape
    run_initial_scrape()

    # 2. Background periodic scraping
    start_scheduler()

    # 3. Production WSGI server
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"[Server] Starting Waitress on http://{host}:{port}")
    serve(app, host=host, port=port)
