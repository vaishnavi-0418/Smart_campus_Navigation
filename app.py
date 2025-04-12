from flask import Flask, jsonify, request
import mysql.connector
import heapq

app = Flask(__name__)

# -------------------- DB Connection --------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # Change if your username is different
        password="root",   # ← REPLACE with your actual MySQL password
        database="smart_campus"    # ← Use your actual DB name
    )

# -------------------- GET /locations --------------------
@app.route("/locations", methods=["GET"])
def get_locations():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT location_id, name FROM locations")
    rows = cursor.fetchall()
    db.close()

    locations = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify({"locations": locations})


# -------------------- Build Graph from DB --------------------
def get_graph_from_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT from_location, to_location, total_distance FROM paths")
    rows = cursor.fetchall()
    db.close()

    graph = {}
    for from_node, to_node, dist in rows:
        if from_node not in graph:
            graph[from_node] = []
        if to_node not in graph:
            graph[to_node] = []
        
        # Undirected graph: both directions
        graph[from_node].append((to_node, dist))
        graph[to_node].append((from_node, dist))

    return graph


# -------------------- A* Pathfinding Logic --------------------
def a_star(graph, start, end):
    queue = [(0, start, [])]  # (cost, current, path)
    visited = set()

    while queue:
        cost, current, path = heapq.heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        path = path + [current]

        if current == end:
            return path, cost

        for neighbor, distance in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + distance, neighbor, path))

    return None, float('inf')


# -------------------- POST /find_path --------------------
@app.route("/find_path", methods=["POST"])
def find_path():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        return jsonify({"error": "Start and End IDs required"}), 400

    graph = get_graph_from_db()
    path, total_distance = a_star(graph, start, end)

    if not path:
        return jsonify({"error": "No path found"}), 404

    # Get names of locations in the path
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT location_id, name FROM locations")
    location_map = dict(cursor.fetchall())
    db.close()

    path_names = [location_map[node] for node in path]

    return jsonify({
        "path": path_names,
        "distance": total_distance
    })


# -------------------- Home Route --------------------
@app.route("/")
def home():
    return jsonify({"message": "Smart Campus backend is working!"})


# -------------------- Start Server --------------------
if __name__ == "__main__":
    app.run(debug=True)
