from flask import Flask, jsonify, redirect, render_template, request
import os

app = Flask(__name__)

# In-memory storage with unique integer IDs
itineraries = [
    {
        "id": 1,
        "destination": "Goa",
        "day": "Day 1",
        "activity": "Visit Baga Beach",
        "notes": "Evening visit"
    }
]

next_id = 2


@app.route("/", methods=["GET"])
def home():
    commit_id = os.getenv("RENDER_GIT_COMMIT", "local")
    return render_template(
        "index.html",
        itineraries=itineraries,
        commit_id=commit_id
    )


@app.route("/add", methods=["POST"])
def add_itinerary():
    global next_id
    destination = request.form.get("destination", "").strip()
    day = request.form.get("day", "").strip()
    activity = request.form.get("activity", "").strip()
    notes = request.form.get("notes", "").strip()

    if not destination or not day or not activity:
        return "Destination, day, and activity are required.", 400

    itineraries.append({
        "id": next_id,
        "destination": destination,
        "day": day,
        "activity": activity,
        "notes": notes
    })
    next_id += 1

    return redirect("/")


@app.route("/update/<int:item_id>", methods=["POST"])
def update_itinerary(item_id):
    destination = request.form.get("destination", "").strip()
    day = request.form.get("day", "").strip()
    activity = request.form.get("activity", "").strip()
    notes = request.form.get("notes", "").strip()

    if not destination or not day or not activity:
        return "Destination, day, and activity are required.", 400

    for item in itineraries:
        if item["id"] == item_id:
            item["destination"] = destination
            item["day"] = day
            item["activity"] = activity
            item["notes"] = notes
            break

    return redirect("/")


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_itinerary(item_id):
    global itineraries
    itineraries = [item for item in itineraries if item["id"] != item_id]
    return redirect("/")


@app.route("/api/itineraries", methods=["GET"])
def api_itineraries():
    return jsonify(itineraries)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
