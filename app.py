from flask import Flask, jsonify, request
import mysql.connector
import heapq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    cursor.close()
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
    path, _ = a_star(graph, start, end)

    if not path or len(path) < 2:
        return jsonify({"error": "No path found"}), 404

    db = connect_db()
    cursor = db.cursor()

    # Get names of locations
    cursor.execute("SELECT location_id, name FROM locations")
    location_map = dict(cursor.fetchall())

    all_steps = []
    total_distance = 0

    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        
        print(f"Searching path_id for: {from_node} -> {to_node}")

        # Get path_id for the segment (either direction)
        cursor.execute("""
            SELECT path_id FROM paths
            WHERE (from_location = %s AND to_location = %s)
               OR (from_location = %s AND to_location = %s)
            LIMIT 1
        """, (from_node, to_node, to_node, from_node))
        result = cursor.fetchone()
        

        if result:
            path_id = result[0]
            print("Found path_id:", path_id)
            # Fetch all steps for this path_id
            cursor.execute("""
                SELECT instruction, distance FROM path_steps
                WHERE path_id = %s ORDER BY step_order
            """, (path_id,))
            step_rows = cursor.fetchall()
            print("Fetched steps:", step_rows)
  

            for instruction, distance in step_rows:
                all_steps.append({
                    "instruction": instruction,
                    "distance": distance
                })
                total_distance += distance
        else:
            # fallback if no path_id found
            all_steps.append({
                "instruction": f"Move from {location_map[from_node]} to {location_map[to_node]}",
                "distance": 0
            })

    db.close()

    return jsonify({
        "path": [location_map[node] for node in path],
        "total_distance": total_distance,
        "steps": all_steps
    })

# -------------------- Home Route --------------------
@app.route("/")
def home():
    return jsonify({"message": "Smart Campus backend is working!"})


# -------------------- Start Server --------------------
if __name__ == "__main__":
    app.run(debug=True)
