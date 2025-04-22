from flask import Flask, jsonify, request
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

app = Flask(__name__)

API_TOKEN = "feather987oak"

def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

geolocator = Nominatim(user_agent="capital-time-api")
tf = TimezoneFinder()

@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    try:
        location = geolocator.geocode(city)
        if not location:
            return jsonify({"error": f"City '{city}' not found"}), 404

        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        if not timezone_str:
            return jsonify({"error": "Timezone could not be determined"}), 500

        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        offset = now.strftime('%z')
        formatted_offset = f"{offset[:3]}:{offset[3:]}"
        return jsonify({
            "city": city,
            "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
            "utc_offset": formatted_offset
        })

    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
