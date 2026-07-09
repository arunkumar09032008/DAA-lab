from flask import Flask, render_template_string, request, jsonify
import heapq
import random
import time

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
    edges.sort()  # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0
    steps = []
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            steps.append({"action": "add", "u": u, "v": v, "weight": w, "cost": cost})
        else:
            steps.append({"action": "skip", "u": u, "v": v, "weight": w})
        if len(mst) == n - 1:
            break
    return mst, cost, steps


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
    steps = []
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
            steps.append({"action": "add", "u": parent[u], "v": u, "weight": w, "cost": cost})
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost, steps


def build_adj(n, edges):
    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ex. 03 — Minimum Spanning Tree</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --accent: #58a6ff; --green: #3fb950; --orange: #f0883e;
    --red: #f85149; --purple: #bc8cff; --yellow: #e3b341;
    --text: #e6edf3; --muted: #8b949e; --danger: #f85149;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; }
  header { border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; display: flex; align-items: center; gap: 1rem; }
  .badge { background: var(--green); color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 4px; }
  header h1 { font-size: 1.1rem; font-weight: 600; }
  header p { font-size: 0.8rem; color: var(--muted); margin-top: 0.15rem; }
  main { max-width: 1100px; margin: 0 auto; padding: 2rem; }
  section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
  section h2 { font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
  .row { display: flex; gap: 1rem; flex-wrap: wrap; }
  .field { flex: 1; min-width: 200px; }
  label { display: block; font-size: 0.8rem; color: var(--muted); margin-bottom: 0.4rem; font-family: 'JetBrains Mono', monospace; }
  input, textarea { width: 100%; background: var(--bg); border: 1px solid var(--border); color: var(--text); padding: 0.6rem 0.8rem; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; outline: none; transition: border-color 0.2s; resize: vertical; }
  input:focus, textarea:focus { border-color: var(--green); }
  .btn { background: var(--green); color: #000; border: none; padding: 0.65rem 1.4rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: opacity 0.2s; }
  .btn:hover { opacity: 0.85; }
  .btn-outline { background: transparent; color: var(--green); border: 1px solid var(--green); }
  .btn-orange { background: var(--orange); }
  .btn-orange.btn-outline { background: transparent; color: var(--orange); border: 1px solid var(--orange); }
  .gap { margin-top: 0.8rem; display: flex; gap: 0.8rem; flex-wrap: wrap; }
  .algo-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem; }
  .algo-card { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; }
  .algo-card h3 { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.8rem; font-family: 'JetBrains Mono', monospace; }
  .algo-card.kruskal h3 { color: var(--accent); }
  .algo-card.prim h3 { color: var(--orange); }
  .stat-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-bottom: 0.35rem; }
  .stat-row span:first-child { color: var(--muted); }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); color: var(--muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace; }
  td { padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; }
  tr:last-child td { border-bottom: none; }
  .kruskal-col { color: var(--accent); } .prim-col { color: var(--orange); }
  .best { font-weight: 700; color: var(--green); }
  .edge-table { margin-top: 0.6rem; }
  .edge-table td { font-size: 0.8rem; padding: 0.35rem 0.6rem; }
  .edge-table th { font-size: 0.7rem; padding: 0.35rem 0.6rem; }
  .cost-badge { display: inline-block; background: var(--green); color: #000; border-radius: 999px; font-size: 0.85rem; font-weight: 700; padding: 2px 12px; font-family: 'JetBrains Mono', monospace; }
  .skipped { opacity: 0.4; text-decoration: line-through; }
  canvas { display: block; width: 100%; border-radius: 8px; background: var(--bg); border: 1px solid var(--border); }
  .canvas-container { position: relative; margin-top: 1rem; }
  .legend { display: flex; gap: 1.2rem; margin-top: 0.8rem; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 0.4rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--muted); }
  .legend-dot { width: 12px; height: 4px; border-radius: 2px; }
  .loading { color: var(--muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }
  @media(max-width:640px) { .algo-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <div><div class="badge">EX. 03</div></div>
  <div>
    <h1>Minimum Spanning Tree</h1>
    <p>Kruskal's &amp; Prim's Algorithms — CS5303 DAA Lab</p>
  </div>
</header>
<main>
  <section>
    <h2>Graph Definition</h2>
    <div class="row">
      <div class="field">
        <label>Edges (weight, u, v) — one per line</label>
        <textarea id="edgesInput" rows="5">7,0,1
5,0,3
8,1,2
9,1,3
7,1,4
5,2,4
15,3,4
6,3,5
8,4,5
9,4,6
11,5,6</textarea>
      </div>
      <div class="field" style="max-width:120px">
        <label>Nodes (n)</label>
        <input id="nodesInput" type="number" value="7" min="2" max="20">
      </div>
    </div>
    <div class="gap">
      <button class="btn" onclick="runMST()">Compute MST</button>
      <button class="btn btn-outline" onclick="randomGraph()">Random Graph</button>
    </div>
  </section>

  <section>
    <h2>Graph Visualization</h2>
    <div class="canvas-container">
      <canvas id="graphCanvas" width="700" height="420"></canvas>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:var(--muted)"></div>Not in MST</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--accent)"></div>Kruskal's MST</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--orange)"></div>Prim's MST</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--green)"></div>Shared by both</div>
    </div>
  </section>

  <section>
    <h2>Results</h2>
    <div id="resultsArea">
      <p class="loading">Click "Compute MST" to see results.</p>
    </div>
  </section>
</main>
<script>
const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
let nodePositions = [];
let graphData = null;

function randomGraph() {
  const n = 5 + Math.floor(Math.random() * 4);
  document.getElementById('nodesInput').value = n;
  const edges = [];
  const nodes = Array.from({length: n}, (_, i) => i);
  for (let i = 0; i < n - 1; i++) {
    edges.push([1 + Math.floor(Math.random() * 20), nodes[i], nodes[i + 1]]);
  }
  const extra = 2 + Math.floor(Math.random() * 4);
  for (let i = 0; i < extra; i++) {
    const u = Math.floor(Math.random() * n);
    let v = Math.floor(Math.random() * n);
    while (v === u) v = Math.floor(Math.random() * n);
    edges.push([1 + Math.floor(Math.random() * 20), u, v]);
  }
  document.getElementById('edgesInput').value = edges.map(e => e.join(',')).join('\n');
}

function runMST() {
  const edgesRaw = document.getElementById('edgesInput').value.trim();
  const n = parseInt(document.getElementById('nodesInput').value);
  if (!edgesRaw || !n) return;
  const edges = edgesRaw.split('\n').map(line => {
    const parts = line.split(',').map(s => parseInt(s.trim()));
    return { weight: parts[0], u: parts[1], v: parts[2] };
  }).filter(e => !isNaN(e.weight) && !isNaN(e.u) && !isNaN(e.v));

  fetch('/compute', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({n, edges})
  }).then(r => r.json()).then(data => {
    drawGraph(n, edges, data);
    renderResults(data);
  });
}

function layoutNodes(n) {
  const positions = [];
  const cx = 350;
  const cy = 210;
  const r = Math.min(cx, cy) * 0.7;
  for (let i = 0; i < n; i++) {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    positions.push({ x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) });
  }
  return positions;
}

let canvasInitialized = false;
function initCanvas() {
  if (canvasInitialized) return;
  canvasInitialized = true;
  const dpr = window.devicePixelRatio || 1;
  canvas.width = 700 * dpr;
  canvas.height = 420 * dpr;
  canvas.style.width = '700px';
  canvas.style.height = '420px';
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
function drawGraph(n, edges, data) {
  initCanvas();

  ctx.clearRect(0, 0, 700, 420);
  const positions = layoutNodes(n);
  nodePositions = positions;

  // Determine MST edges
  const kSet = new Set();
  const pSet = new Set();
  const sSet = new Set();
  data.kruskal.mst.forEach(e => { kSet.add(e.u + '-' + e.v); kSet.add(e.v + '-' + e.u); });
  data.prim.mst.forEach(e => { pSet.add(e.u + '-' + e.v); pSet.add(e.v + '-' + e.u); });
  kSet.forEach(k => { if (pSet.has(k)) sSet.add(k); });

  // Draw all edges
  edges.forEach(e => {
    const key1 = e.u + '-' + e.v;
    const key2 = e.v + '-' + e.u;
    const inK = kSet.has(key1);
    const inP = pSet.has(key1);
    const shared = sSet.has(key1);

    ctx.beginPath();
    ctx.moveTo(positions[e.u].x, positions[e.u].y);
    ctx.lineTo(positions[e.v].x, positions[e.v].y);

    if (shared) {
      ctx.strokeStyle = '#3fb950';
      ctx.lineWidth = 3;
    } else if (inK) {
      ctx.strokeStyle = '#58a6ff';
      ctx.lineWidth = 2.5;
    } else if (inP) {
      ctx.strokeStyle = '#f0883e';
      ctx.lineWidth = 2.5;
    } else {
      ctx.strokeStyle = '#30363d';
      ctx.lineWidth = 1;
    }
    ctx.stroke();

    // Weight label
    const mx = (positions[e.u].x + positions[e.v].x) / 2;
    const my = (positions[e.u].y + positions[e.v].y) / 2;
    ctx.font = '600 11px JetBrains Mono, monospace';
    ctx.fillStyle = shared ? '#3fb950' : (inK || inP ? '#e6edf3' : '#6e7681');
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(e.weight, mx, my - 8);
  });

  // Draw nodes
  positions.forEach((p, i) => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 18, 0, 2 * Math.PI);
    ctx.fillStyle = '#161b22';
    ctx.fill();
    ctx.strokeStyle = '#58a6ff';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.font = '700 13px JetBrains Mono, monospace';
    ctx.fillStyle = '#e6edf3';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(i, p.x, p.y);
  });
}

function renderResults(data) {
  let html = '<div class="algo-grid">';

  // Kruskal card
  html += '<div class="algo-card kruskal"><h3>Kruskal\'s Algorithm</h3>';
  html += '<div class="stat-row"><span>Total Cost</span><span class="cost-badge" style="background:var(--accent)">' + data.kruskal.cost + '</span></div>';
  html += '<div class="stat-row"><span>Edges in MST</span><span>' + data.kruskal.mst.length + '</span></div>';
  html += '<table class="edge-table"><thead><tr><th>Edge</th><th>Weight</th></tr></thead><tbody>';
  data.kruskal.steps.forEach(s => {
    if (s.action === 'add') {
      html += '<tr><td>(' + s.u + ' — ' + s.v + ')</td><td style="color:var(--accent)">' + s.weight + '</td></tr>';
    }
  });
  html += '</tbody></table></div>';

  // Prim card
  html += '<div class="algo-card prim"><h3>Prim\'s Algorithm</h3>';
  html += '<div class="stat-row"><span>Total Cost</span><span class="cost-badge" style="background:var(--orange)">' + data.prim.cost + '</span></div>';
  html += '<div class="stat-row"><span>Edges in MST</span><span>' + data.prim.mst.length + '</span></div>';
  html += '<table class="edge-table"><thead><tr><th>Edge</th><th>Weight</th></tr></thead><tbody>';
  data.prim.steps.forEach(s => {
    if (s.action === 'add') {
      html += '<tr><td>(' + s.u + ' — ' + s.v + ')</td><td style="color:var(--orange)">' + s.weight + '</td></tr>';
    }
  });
  html += '</tbody></table></div></div>';

  // Comparison note
  const same = data.kruskal.cost === data.prim.cost;
  html += '<div style="margin-top:1rem;text-align:center;font-family:JetBrains Mono,monospace;font-size:0.85rem;color:var(--muted)">';
  html += same
    ? 'Both algorithms produce an MST with the same total cost: <span class="cost-badge" style="margin-left:6px">' + data.kruskal.cost + '</span>'
    : 'Costs differ (should not happen for connected graphs). Kruskal: ' + data.kruskal.cost + ', Prim: ' + data.prim.cost;
  html += '</div>';

  document.getElementById('resultsArea').innerHTML = html;
}
</script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    n = data['n']
    edges = [(e['weight'], e['u'], e['v']) for e in data['edges']]
    adj = build_adj(n, edges)

    k_mst, k_cost, k_steps = kruskal(n, edges[:])
    p_mst, p_cost, p_steps = prim(n, adj)

    return jsonify({
        "kruskal": {
            "mst": [{"u": u, "v": v, "w": w} for u, v, w in k_mst],
            "cost": k_cost,
            "steps": k_steps
        },
        "prim": {
            "mst": [{"u": u, "v": v, "w": w} for u, v, w in p_mst],
            "cost": p_cost,
            "steps": p_steps
        }
    })


if __name__ == '__main__':
    app.run(debug=True)