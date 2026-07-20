import heapq
from flask import Flask, render_template_string

app = Flask(__name__)


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path[0] == source:
        return path
    return []


# --- Graph Definition (Adjacency List) ---
GRAPH = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}
SOURCE = 0


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Dijkstra's Shortest Path</title>
<style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; background: #f7f7f9; color: #222; }
    h1 { text-align: center; }
    .card { background: #fff; border-radius: 10px; padding: 20px 30px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid #eee; }
    th { background: #f0f0f5; }
</style>
</head>
<body>
    <h1>Dijkstra's Shortest Path</h1>
    <div class="card">
        <h2>Shortest paths from vertex {{ src }}</h2>
        <table>
            <tr><th>Vertex</th><th>Distance</th><th>Path</th></tr>
            {% for v, d, p in rows %}
            <tr><td>{{ v }}</td><td>{{ d }}</td><td>{{ p }}</td></tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    dist, prev = dijkstra(GRAPH, SOURCE)
    rows = []
    for v in range(len(GRAPH)):
        path = reconstruct_path(prev, SOURCE, v)
        path_str = ' -> '.join(map(str, path)) if path else 'No path'
        d = dist[v] if dist[v] != float('inf') else 'INF'
        rows.append((v, d, path_str))
    return render_template_string(PAGE_TEMPLATE, src=SOURCE, rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
