from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta, timezone
import os
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI')

# === Debug checks ===
if not GOOGLE_MAPS_API_KEY:
    print("❌ GOOGLE_MAPS_API_KEY not loaded. Check your .env file.")
else:
    print("✅ GOOGLE_MAPS_API_KEY loaded")

if not SECRET_KEY:
    print("❌ SECRET_KEY not loaded. Check your .env file.")
else:
    print("✅ SECRET_KEY loaded")

if not MONGO_URI:
    print("❌ MONGO_URI not loaded. Check your .env file.")
else:
    print("✅ MONGO_URI loaded")

# === Initialize Flask App ===
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = SECRET_KEY

# === MongoDB connection ===
client = MongoClient(MONGO_URI)
db = client['waysync']
users = db['users']
markers = db['markers']
reached_collection = db['reached_locations']
routes_collection = db['routes']

# ----------------------------
# 🔐 AUTH API ROUTES
# ----------------------------

@app.route('/register', methods=['POST'])
def register_api():
    data = request.json
    if users.find_one({'email': data['email']}):
        return jsonify({'msg': 'User already exists'}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    users.insert_one({
        'username': data['username'],
        'email': data['email'],
        'password': hashed_pw,
        'registered_on': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
    })
    return jsonify({'msg': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login_api():
    data = request.json
    user = users.find_one({'email': data['email']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        session['user'] = user['email']  # ⬅️ store in session
        token = jwt.encode({
            'email': user['email'],
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'msg': 'Invalid credentials'}), 401

# ----------------------------
# 🌐 HTML ROUTES
# ----------------------------

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/')
def home():
    return render_template("about.html")

@app.route('/get-started')
def get_started_page():
    return render_template("get-started.html")

@app.route('/dashboard')
def dashboard_page():
    return render_template("dashboard.html")

@app.route('/features')
def features_page():
    return render_template("features.html")

@app.route('/vision')
def vision_page():
    return render_template("vision.html")

@app.route('/maps')
def maps_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("maps.html")

@app.route('/visited')
def visited_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    all_places = list(reached_collection.find({}, {"_id": 0}))
    return render_template("visited.html", visited=all_places, GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect user to login page

# ----------------------------
# 🛡️ ADMIN DASHBOARD ROUTE
# ----------------------------

@app.route('/admin')
def admin_dashboard():
    all_users = list(users.find({}, {"_id": 0, "username": 1, "email": 1, "registered_on": 1}))
    return render_template("admin.html", users=all_users)

# ----------------------------  
# 🗺️ MAPS API ROUTES
# ----------------------------

@app.route('/api/directions', methods=['GET'])
def get_directions():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # Validate input
    if not origin or not destination:
        return jsonify({"error": "Missing 'origin' or 'destination' parameter."}), 400

    # Prepare Google Maps Directions API URL and params
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }

    # Call Google Directions API
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": "Failed to contact Google Maps API.", "details": str(e)}), 502

    data = response.json()

    # Check if Google Maps returned an error status
    if data.get("status") != "OK":
        return jsonify({
            "error": "Google Maps API error.",
            "status": data.get("status"),
            "details": data.get("error_message", "No additional info")
        }), 400

    # Success: return the full directions response to frontend
    return jsonify(data)

@app.route('/api/save_route', methods=['POST'])
def save_route():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    if not origin or not destination:
        return jsonify({"error": "Missing origin or destination"}), 400

    routes_collection.insert_one({
        "origin": origin,
        "destination": destination,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"message": "Route saved successfully"})

@app.route('/api/markers', methods=['POST'])
def save_marker():
    data = request.json
    markers.insert_one({
        "lat": data["lat"],
        "lng": data["lng"],
        "label": data["label"],
        "created_at": datetime.now(timezone.utc)
    })
    return jsonify({"status": "Marker saved successfully"})

@app.route('/api/markers', methods=['GET'])
def get_all_markers():
    all_markers = list(markers.find({}, {"_id": 0}))
    return jsonify(all_markers)

@app.route('/api/reached', methods=['POST'])
def save_reached_location():
    data = request.json
    lat, lng = data["latitude"], data["longitude"]

    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    geo_res = requests.get(geo_url).json()
    address = geo_res["results"][0]["formatted_address"] if geo_res["results"] else "Unknown"

    location_record = {
        "user": request.headers.get('X-User-Email', 'anonymous'),
        "latitude": lat,
        "longitude": lng,
        "address": address,
        "timestamp": datetime.fromisoformat(data["timestamp"])
    }

    reached_collection.insert_one(location_record)
    return jsonify({"message": "Location + address saved."})

@app.route('/api/traffic', methods=['GET'])
def get_traffic_data():
    return jsonify({"message": "Traffic data endpoint"})

# ----------------------------
# 🗂 Serve static assets
# ----------------------------

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# ----------------------------
# 🚀 Run Flask App
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
