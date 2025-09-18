# Simple Event Manager Backend
# Handcrafted for HackWithHyderabad Problem 6

from flask import Flask, request, jsonify

app = Flask(__name__)

# Just keeping data in memory, easy for demo
event_list = []
participants_map = {}

def generate_event_id():
    # Just a quick ID generator based on count
    return f"EVT{len(event_list) + 101}"

@app.route("/events", methods=["POST"])
def add_event():
    details = request.get_json()
    new_id = generate_event_id()
    event = {
        "id": new_id,
        "title": details.get("name"),
        "date": details.get("date"),
        "tags": details.get("tags", []),
        "created_at": "now-ish"
    }
    event_list.append(event)
    participants_map[new_id] = []
    return jsonify(event), 201

@app.route("/events", methods=["GET"])
def get_events():
    tag_filter = request.args.get("tag")
    if tag_filter:
        filtered = [e for e in event_list if tag_filter in e["tags"]]
        return jsonify(filtered)
    return jsonify(event_list)

@app.route("/events/<event_id>/join", methods=["POST"])
def register_participant(event_id):
    if event_id not in participants_map:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    participant_info = {
        "name": data.get("pname"),
        "email": data.get("email"),
        "skills": data.get("skills", [])
    }
    participants_map[event_id].append(participant_info)
    return jsonify({
        "message": "Thanks for registering!",
        "total_participants": len(participants_map[event_id])
    })

@app.route("/events/<event_id>/stats", methods=["GET"])
def event_statistics(event_id):
    if event_id not in participants_map:
        return jsonify({"error": "No data for this event"}), 404

    participants = participants_map[event_id]
    skill_count = {}
    for person in participants:
        for skill in person.get("skills", []):
            skill_count[skill] = skill_count.get(skill, 0) + 1

    return jsonify({
        "total": len(participants),
        "skill_summary": skill_count
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
