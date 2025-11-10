from flask import Flask, jsonify, request, abort

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # In-memory store; in real life, replace with DB
    state = {"workouts": [], "next_id": 1}

    @app.get("/")
    def root():
        return jsonify({"status": "ok", "service": "ACEest Fitness API"}), 200

    @app.get("/healthz")
    def healthz():
        return "ok", 200

    @app.post("/api/workouts")
    def create_workout():
        data = request.get_json(force=True, silent=True) or {}
        if "name" not in data or "duration" not in data:
            abort(400, "Missing 'name' or 'duration'")
        item = {
            "id": state["next_id"],
            "name": data["name"],
            "duration": int(data["duration"]),
            "calories": int(data.get("calories", 0)),
        }
        state["next_id"] += 1
        state["workouts"].append(item)
        return jsonify(item), 201

    @app.get("/api/workouts")
    def list_workouts():
        return jsonify(state["workouts"]), 200

    @app.get("/api/workouts/<int:wid>")
    def get_workout(wid: int):
        for w in state["workouts"]:
            if w["id"] == wid:
                return jsonify(w), 200
        abort(404)

    @app.delete("/api/workouts/<int:wid>")
    def delete_workout(wid: int):
        before = len(state["workouts"])
        state["workouts"] = [w for w in state["workouts"] if w["id"] != wid]
        if len(state["workouts"]) == before:
            abort(404)
        return "", 204

    return app

# Allow 'flask run' without setting FLASK_APP, or 'python app.py'
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
