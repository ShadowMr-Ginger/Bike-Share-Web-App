# 1. Imports
from flask import Flask, jsonify, request, session
from database import db_manager as dbm
from dotenv import load_dotenv
from sqlalchemy import text
import os
import hashlib
from flask_cors import CORS
import direction
from models import prediction_tools as prt
import joblib

# -----------------------------------------------------
# The web page will load first and then fetch the data.
# When the user clicks on a station will will fetch more info from data base for more detail
# -----------------------------------------------------

# 2. Load .env
load_dotenv()

# 3. Initialize 'app'
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Load from .env

# Get API Keys
google_key = os.getenv("GOOGLE_KEY")
ors_key = os.getenv("ORS_KEY")

# -----------------------------------------------------
# Tools
# -----------------------------------------------------

model=joblib.load("models/bike_availability_model.pkl")

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


# --- Authentication & User Managment --------------------------------------------------


@app.route("/api/auth/signup", methods=["POST"])
def register_user():
    data = request.get_json(force=True, silent=True) or {}

    if not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing email or password"}), 400

    result = dbm.create_user(data)

    if result == 1:
        return (
            jsonify({"success": True, "message": "User registered successfully"}),
            201,
        )
    elif result == -1:
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({"error": "Registration failed: Internal database error"}), 500


@app.route("/api/auth/login", methods=["POST"])
def login():

    creds = request.get_json(force=True, silent=True) or {}

    user = dbm.read_user_security(creds.get("username"))

    if user and user.get("password") == hash_password(creds.get("password", "")):
        session["username"] = user["username"]
        user_data = dbm.read_user_data(user["username"])
        avatar = user_data.get("avatar") or ""
        return jsonify(
            {
                "success": True,
                "id": user_data.get("id"),
                "email": user_data.get("email"),
                "token": user_data.get("token"),
                "avatar": avatar,
            }
        )
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"success": True})


@app.route("/api/user/<username>", methods=["GET", "PUT"])
def user_profile(username):
    if request.method == "GET":
        profile = dbm.read_user_data(username)
        if profile:
            return jsonify(profile)
        return jsonify({"error": "User not found"}), 404
    # PUT
    payload = request.get_json() or {}
    payload["username"] = username
    if dbm.update_user_data(payload) == 1:
        return jsonify({"success": True})
    return jsonify({"error": "Update failed"}), 500


# --- Avatar Upload --------------------------------------------------------------------

AVATAR_DIR = os.path.join(os.path.dirname(__file__), "static", "avatars")
os.makedirs(AVATAR_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/user/<int:user_id>/avatar", methods=["POST"])
def upload_avatar(user_id):
    if "avatar" not in request.files:
        return jsonify({"message": "No file provided"}), 400
    file = request.files["avatar"]
    if not file.filename or not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{user_id}.{ext}"
    file.save(os.path.join(AVATAR_DIR, filename))

    avatar_url = f"/static/avatars/{filename}"
    with dbm.engine.connect() as conn:
        conn.execute(
            text("UPDATE user SET avatar_url=:url WHERE id=:id"),
            {"url": avatar_url, "id": user_id},
        )
        conn.commit()

    return jsonify({"avatar": avatar_url})


# --- Favorites/Saved Stations ---------------------------------------------------------


@app.route("/api/user/<username>/favorites", methods=["GET"])
def get_favorites(username):
    profile = dbm.read_user_data(username)
    if profile:
        return jsonify({"favorites": profile.get("favorites", [])})
    return jsonify({"error": "User not found"}), 404


@app.route(
    "/api/user/<username>/favorites/<int:station_id>", methods=["POST", "DELETE"]
)
def modify_favorite(username, station_id):
    user = dbm.read_user_data(username)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_id = user["id"]
    if request.method == "POST":
        if dbm.write_to_db_favorite(user_id, station_id) == 1:
            return jsonify({"success": True})
        return jsonify({"error": "Failed to add favorite"}), 500
    # DELETE
    with dbm.engine.connect() as conn:
        conn.execute(
            text("DELETE FROM favorite WHERE user_id=:u AND station_number=:n"),
            {"u": user_id, "n": station_id},
        )
        conn.commit()
    return jsonify({"success": True})


# --- Weather Forcasts -----------------------------------------------------------------


@app.route("/api/weather", methods=["GET"])
@app.route("/api/weather/current", methods=["GET"])
def get_current_weather():
    """
    This loads immediately after the HTML is fully loaded.
    RETURNS JSON of the current weather in Dublin from DB.
    """

    try:
        weather_data = dbm.read_current_weather()

        if not weather_data:
            return jsonify({"error": "Weather data not available"}), 404

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/weather/forecast/hourly", methods=["GET"])
@app.route("/api/weather/hourly", methods=["GET"])
def get_forecast_hourly():
    return jsonify(dbm.read_forecast_hourly())


@app.route("/api/weather/forecast/daily", methods=["GET"])
@app.route("/api/weather/daily", methods=["GET"])
def get_forecast_daily():
    dailyWeather = dbm.read_forecast_daily()
    return jsonify({"daily": dailyWeather})


# --- Station Retreval -----------------------------------------------------------------


@app.route("/api/stations")
def get_all_stations():
    try:
        raw_stations = dbm.read_stations()
        # Just return the list directly; it already contains 'lat', 'lng', and 'id'
        return jsonify(raw_stations)

    except Exception as e:
        print(f"Error fetching stations: {e}")
        return jsonify({"error": "Failed to fetch stations"}), 500


# When user clicks on a station


@app.route("/api/station/<int:station_id>/history")
def get_station_history(station_id):
    try:
        result = dbm.read_station_history(station_id)

        if result is None:
            return jsonify({"error": "Station not found or DB error"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Daily Average
@app.route("/api/station/<int:station_id>/daily-average")
def get_daily_average(station_id):
    try:
        result = dbm.read_daily_average(station_id)

        if result is None:
            return jsonify({"error": "Station not found or DB error"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Hourly Forecast
@app.route("/api/station/<int:station_id>/hourly-forecast")
def get_hourly_forecast(station_id):
    try:
        (station,weather)=dbm.read_for_prediction(station_id)
        if station is None or weather is None:
            return jsonify({"error": "Station not found or DB error"}), 404
        
        df=prt.data_processor(station,weather)
        if df is None:
            return jsonify({"error": "Data processing failed"}), 500
        
        result=prt.predict_next10(model,df)
        if result is None:
            return jsonify({"error": "Prediction failed"}), 500
        
        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Get Direction --------------------------------------------------------------------------
@app.route("/api/route", methods=["POST"])
def route():
    """
    Data example
    {
        "from": "D02 X285",
        "to": "Dublin City University"
    }
    """
    data = request.json
    from_addr = data.get("from")
    to_addr = data.get("to")

    if not from_addr or not to_addr:
        return jsonify({"message": "from/to required"}), 400

    try:
        result = direction.get_route(from_addr, to_addr)
        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500



# -- Run Configuration ---


if __name__ == "__main__":
    # HOST='0.0.0.0' is crucial for EC2
    # Makes it so that the site is available externally
    app.run(host="0.0.0.0", port=5000, debug=False)
