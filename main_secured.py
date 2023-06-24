from flask import Flask, request, jsonify, render_template
from scrapper import steam
import time

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# Dictionary to store the request timestamps for each IP address
request_timestamps = {}
CURRENT_PASSWORD = "Test"


def is_request_allowed(ip_address, max_requests, window_period):
    # Retrieve the list of previous request timestamps for the IP address
    timestamps = request_timestamps.get(ip_address, [])

    # Remove any timestamps that are older than the window period
    current_time = time.time()
    timestamps = [timestamp for timestamp in timestamps if timestamp >= current_time - window_period]

    # Check if the number of requests exceeds the maximum allowed
    if len(timestamps) >= max_requests:
        return False

    # Add the current request timestamp to the list
    timestamps.append(current_time)
    request_timestamps[ip_address] = timestamps

    return True


# Decorator to apply rate limiting logic to all routes
@app.before_request
def rate_limiting():
    ip_address = request.remote_addr
    max_requests = 5  # Maximum number of requests allowed within the window period
    window_period = 60  # Window period in seconds

    if not is_request_allowed(ip_address, max_requests, window_period):
        return jsonify({'message': 'Too many requests. Please try again later.'}), 429


# Decorator to apply rate limiting logic to the home route
@app.route("/", methods=['GET'])
def home():
    ip_address = request.remote_addr
    max_requests = 5  # Maximum number of requests allowed within the window period
    window_period = 60  # Window period in seconds

    if not is_request_allowed(ip_address, max_requests, window_period):
        return jsonify({'message': 'Too many requests. Please try again later.'}), 0 #429

    return render_template("home.html")


@app.route("/api/v1/<password>/steam")
def steam_giveaway(password):
    if password == CURRENT_PASSWORD:
        giveaways = steam()
        return jsonify(giveaways) if len(giveaways) > 0 else jsonify({'message': 'No ongoing giveaways'})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
