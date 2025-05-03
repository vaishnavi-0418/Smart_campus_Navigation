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
        password="root",           # ← REPLACE with your actual MySQL password
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

    # ---- Find all possible paths (simple DFS, not full optimization) ----
    def dfs(current, end, visited, path, all_paths):
        visited.add(current)
        path.append(current)

        if current == end:
            all_paths.append(list(path))
        else:
            for neighbor, _ in graph.get(current, []):
                if neighbor not in visited:
                    dfs(neighbor, end, visited, path, all_paths)

        path.pop()
        visited.remove(current)

    all_possible_paths = []
    dfs(start, end, set(), [], all_possible_paths)

    if not all_possible_paths:
        return jsonify({"error": "No paths found"}), 404

    # ---- Now calculate distance for each path ----
    db = connect_db()
    cursor = db.cursor()

    # Fetch location names
    cursor.execute("SELECT location_id, name FROM locations")
    location_map = dict(cursor.fetchall())

    paths_info = []

    for path in all_possible_paths:
        path_info = {
            "path": [location_map[node] for node in path],
            "steps": [],
            "total_distance": 0
        }

        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]

            cursor.execute("""
                SELECT path_id FROM paths
                WHERE (from_location = %s AND to_location = %s)
                   OR (from_location = %s AND to_location = %s)
                LIMIT 1
            """, (from_node, to_node, to_node, from_node))
            result = cursor.fetchone()

            if result:
                path_id = result[0]
                # Fetch steps
                cursor.execute("""
                    SELECT instruction, distance FROM path_steps
                    WHERE path_id = %s ORDER BY step_order
                """, (path_id,))
                step_rows = cursor.fetchall()

                for instruction, distance in step_rows:
                    path_info["steps"].append({
                        "instruction": instruction,
                        "distance": distance
                    })
                    path_info["total_distance"] += distance
            else:
                # fallback if no steps
                path_info["steps"].append({
                    "instruction": f"Move from {location_map[from_node]} to {location_map[to_node]}",
                    "distance": 0
                })

        paths_info.append(path_info)

    db.close()

    # ---- Now separate best path and other paths ----
    paths_info.sort(key=lambda p: p["total_distance"])  # Sort by total distance

    best_path = paths_info[0]
    other_paths = paths_info[1:]

    return jsonify({
        "best_path": best_path,
        "other_paths": other_paths
    })

# -------------------- Start Server --------------------
if __name__ == "__main__":
    app.run(debug=True)
