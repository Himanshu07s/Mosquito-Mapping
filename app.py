from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db
import json
import os

app = Flask(__name__)

# Firebase Initialization

if "FIREBASE_KEY" in os.environ:
    firebase_config = json.loads(os.environ["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_config)
else:
    cred = credentials.Certificate("firebase-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://mosquito-mapping-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

@app.route("/")
def dashboard():

    ref = db.reference("/")
    data = ref.get()

    nodes = []

    high_count = 0
    medium_count = 0
    low_count = 0

    if data:

        for key, value in data.items():

            score = value.get("MosquitoScore", 0)

            if score >= 70:
                status = "High"
                high_count += 1

            elif score >= 30:
                status = "Medium"
                medium_count += 1

            else:
                status = "Low"
                low_count += 1

            nodes.append({
                "name": key,
                "temperature": value.get("Temperature", 0),
                "humidity": value.get("Humidity", 0),
                "rain": value.get("RainCondition", ""),
                "audio": value.get("AudioConfidence", 0),
                "score": score,
                "status": status,
                "recommendation": value.get("FoggingRecommendation", "")
            })

    return render_template(
        "dashboard.html",
        nodes=nodes,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )
if __name__ == "__main__":
    app.run(debug=True)