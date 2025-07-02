# Im Gegensatz zum ursprünglichen Code wird die Footprint-Matrix nicht 
# mehr beim Eintreffen der Daten in /store aktualisiert.
# Stattdessen wird sie erst bei einem GET-Request an /footprint 
# dynamisch aus dem aktuellen data_store berechnet.
from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = {}  # {"a": [{"timestamp": "...", "caseid": "...", "activity": "...", "node": "...", "used_as_predecessor": False}, ...]}

@app.route("/store", methods=["POST"])
def store_data():
    data = request.json
    if not data or "node" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    node_name = data["node"]

    if node_name not in data_store:
        data_store[node_name] = []
    
    event = {
        "timestamp": data["timestamp"],
        "caseid": data["caseid"],
        "activity": data["activity"],
        "node": data["node"],
        "used_as_predecessor": False
    }

    data_store[node_name].append(event)
    print(f"Stored data for node {node_name}: {event}")
    
    return jsonify({"message": "Data stored successfully"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data_store), 200

@app.route("/footprint", methods=["GET"])
def get_footprint():
    # Dynamische Generierung der footprint_matrix
    footprint_matrix = {}

    # Alle Nodes initialisieren
    nodes = list(data_store.keys())
    for node in nodes:
        footprint_matrix[node] = {other_node: 0 for other_node in nodes}

    # Temporäre Kopie der Events, um "used_as_predecessor" lokal zu setzen
    temp_store = {node: [dict(e) for e in events] for node, events in data_store.items()}

    for node_name, events in temp_store.items():
        for event in events:
            best_predecessor = None
            best_ts = None

            for other_node, other_events in temp_store.items():
                if other_node == node_name:
                    continue
                for candidate in other_events:
                    if candidate["caseid"] == event["caseid"] and candidate["timestamp"] < event["timestamp"] and not candidate["used_as_predecessor"]:
                        if best_ts is None or candidate["timestamp"] > best_ts:
                            best_predecessor = candidate
                            best_ts = candidate["timestamp"]

            if best_predecessor:
                best_predecessor["used_as_predecessor"] = True
                footprint_matrix[node_name][best_predecessor["node"]] += 1

    return jsonify(footprint_matrix), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
