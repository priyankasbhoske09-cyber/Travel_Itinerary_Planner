from flask import Flask, jsonify, redirect, render_template, request
import os

app = Flask(__name__)

itineraries = [
    {
        "destination": "Goa",
        "day": "Day 1",
        "activity": "Visit Baga Beach",
        "notes": "Evening visit"
    }
]


@app.route("/")
def home():
    commit_id = os.getenv("RENDER_GIT_COMMIT", "local")
    return render_template("index.html", itineraries=itineraries, commit_id=commit_id)


@app.route("/add", methods=["POST"])
def add_itinerary():
    destination = request.form.get("destination", "").strip()
    day = request.form.get("day", "").strip()
    activity = request.form.get("activity", "").strip()
    notes = request.form.get("notes", "").strip()

    if not destination or not day or not activity:
        return "Destination, day and activity are required.", 400

    itineraries.append({
        "destination": destination,
        "day": day,
        "activity": activity,
        "notes": notes
    })

    return redirect("/")


@app.route("/api/itineraries")
def api_itineraries():
    return jsonify(itineraries)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    