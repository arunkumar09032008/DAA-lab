import heapq
from flask import Flask, render_template_string

app = Flask(__name__)


# --- Union-Find for Kruskal ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n, edges):
    """edges: list of (weight, u, v)"""
    edges = sorted(edges)  # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost


def prim(n, adj, start=0):
    """adj: adjacency list {u: [(v, w), ...]}"""
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost


# --- Graph Definition ---
N = 7
EDGES = [
    (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
    (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
    (8, 4, 5), (9, 4, 6), (11, 5, 6)
]

ADJ = {}
for w, u, v in EDGES:
    ADJ.setdefault(u, []).append((v, w))
    ADJ.setdefault(v, []).append((u, w))


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MST - Kruskal &amp; Prim</title>
<style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; background: #f7f7f9; color: #222; }
    h1 { text-align: center; }
    .card { background: #fff; border-radius: 10px; padding: 20px 30px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid #eee; }
    th { background: #f0f0f5; }
    .cost { font-weight: bold; font-size: 1.1em; margin-top: 10px; }
</style>
</head>
<body>
    <h1>Minimum Spanning Tree</h1>

    <div class="card">
        <h2>Kruskal's Algorithm</h2>
        <table>
            <tr><th>Edge</th><th>Weight</th></tr>
            {% for u, v, w in k_mst %}
            <tr><td>{{ u }} - {{ v }}</td><td>{{ w }}</td></tr>
            {% endfor %}
        </table>
        <div class="cost">Total Cost: {{ k_cost }}</div>
    </div>

    <div class="card">
        <h2>Prim's Algorithm</h2>
        <table>
            <tr><th>Edge</th><th>Weight</th></tr>
            {% for u, v, w in p_mst %}
            <tr><td>{{ u }} - {{ v }}</td><td>{{ w }}</td></tr>
            {% endfor %}
        </table>
        <div class="cost">Total Cost: {{ p_cost }}</div>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    k_mst, k_cost = kruskal(N, EDGES[:])
    p_mst, p_cost = prim(N, ADJ)
    return render_template_string(
        PAGE_TEMPLATE, k_mst=k_mst, k_cost=k_cost, p_mst=p_mst, p_cost=p_cost
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)