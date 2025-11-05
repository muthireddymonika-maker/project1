from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random, time

app = Flask(__name__)
CORS(app)

otp_storage = {}  # Store OTP temporarily

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    otp = str(random.randint(100000, 999999))
    otp_storage[phone] = {"otp": otp, "time": time.time()}

    print(f"OTP for {phone} is {otp}")  # simulate sending SMS
    return jsonify({"message": "OTP sent successfully"}), 200

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone = data.get('phone')
    otp = data.get('otp')

    if not phone or not otp:
        return jsonify({"error": "Phone and OTP required"}), 400

    stored = otp_storage.get(phone)
    if stored and stored["otp"] == otp and time.time() - stored["time"] <= 160:
        return jsonify({"message": "OTP verified successfully"}), 200
    else:
        return jsonify({"error": "Invalid or expired OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True)
