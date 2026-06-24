from flask import Flask, render_template_string, request, jsonify
import time
import random

app = Flask(__name__)

def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    steps = []
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                steps.append({"pos": low, "action": "Found target!"})
                return low, comparisons, steps
            return -1, comparisons, steps
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        steps.append({"low": low, "high": high, "pos": pos, "val": arr[pos]})
        if arr[pos] == target:
            return pos, comparisons, steps
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, comparisons, steps

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []
    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]
        start = time.perf_counter()
        for _ in range(100):
            idx_is, comp_is, _ = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000
        start = time.perf_counter()
        for _ in range(100):
            idx_bs, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000
        results.append({
            "size": size,
            "is_time": round(is_time, 4),
            "bs_time": round(bs_time, 4),
            "is_comp": comp_is,
            "bs_comp": comp_bs
        })
    return results

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ex. 01 — Interpolation Search</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --accent: #58a6ff; --green: #3fb950; --orange: #f0883e;
    --text: #e6edf3; --muted: #8b949e; --danger: #f85149;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; }
  header { border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; display: flex; align-items: center; gap: 1rem; }
  .badge { background: var(--accent); color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 4px; }
  header h1 { font-size: 1.1rem; font-weight: 600; }
  header p { font-size: 0.8rem; color: var(--muted); margin-top: 0.15rem; }
  main { max-width: 960px; margin: 0 auto; padding: 2rem; }
  section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
  section h2 { font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
  .row { display: flex; gap: 1rem; flex-wrap: wrap; }
  .field { flex: 1; min-width: 200px; }
  label { display: block; font-size: 0.8rem; color: var(--muted); margin-bottom: 0.4rem; font-family: 'JetBrains Mono', monospace; }
  input { width: 100%; background: var(--bg); border: 1px solid var(--border); color: var(--text); padding: 0.6rem 0.8rem; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; outline: none; transition: border-color 0.2s; }
  input:focus { border-color: var(--accent); }
  .btn { background: var(--accent); color: #000; border: none; padding: 0.65rem 1.4rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: opacity 0.2s; }
  .btn:hover { opacity: 0.85; }
  .btn-outline { background: transparent; color: var(--accent); border: 1px solid var(--accent); }
  .result-box { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 1rem 1.2rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; margin-top: 1rem; display: none; }
  .result-box.show { display: block; }
  .tag-found { color: var(--green); } .tag-miss { color: var(--danger); }
  .vis { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 1rem; }
  .cell { min-width: 38px; padding: 4px 6px; border-radius: 4px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; background: var(--border); color: var(--text); transition: background 0.3s; }
  .cell.probe { background: var(--orange); color: #000; }
  .cell.found { background: var(--green); color: #000; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); color: var(--muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace; }
  td { padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; }
  tr:last-child td { border-bottom: none; }
  .is-col { color: var(--accent); } .bs-col { color: var(--orange); }
  .faster { font-weight: 700; color: var(--green); }
  .loading { color: var(--muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }
  .gap { margin-top: 0.8rem; }
  .bar-wrap { margin-top: 0.5rem; }
  .bar-label { font-size: 0.75rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 2px; }
  .bar { height: 14px; border-radius: 3px; transition: width 0.6s ease; }
  .bar-is { background: var(--accent); }
  .bar-bs { background: var(--orange); }
</style>
</head>
<body>
<header>
  <div>
    <div class="badge">EX. 01</div>
  </div>
  <div>
    <h1>Interpolation Search</h1>
    <p>Implementation &amp; Performance Analysis — CS5303 DAA Lab</p>
  </div>
</header>
<main>
  <section>
    <h2>Live Search</h2>
    <div class="row">
      <div class="field">
        <label>Array (comma-separated integers)</label>
        <input id="arrInput" value="2,5,10,15,23,35,48,60,75,90,105,120">
      </div>
      <div class="field" style="max-width:160px">
        <label>Target</label>
        <input id="targetInput" value="35">
      </div>
    </div>
    <div class="gap">
      <button class="btn" onclick="runSearch()">Run Search</button>
    </div>
    <div class="result-box" id="resultBox"></div>
    <div class="vis" id="vis"></div>
  </section>

  <section>
    <h2>Performance Benchmark</h2>
    <p style="font-size:0.82rem;color:var(--muted);margin-bottom:1rem;">Runs 100 iterations per size on uniformly distributed sorted arrays. IS = Interpolation Search, BS = Binary Search.</p>
    <button class="btn btn-outline" onclick="runBenchmark()">Run Benchmark</button>
    <div id="benchOutput" style="margin-top:1.2rem;"></div>
  </section>
</main>
<script>
function runSearch() {
  const raw = document.getElementById('arrInput').value;
  const target = parseInt(document.getElementById('targetInput').value);
  const arr = raw.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
  fetch('/search', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({arr, target})
  }).then(r => r.json()).then(data => {
    const box = document.getElementById('resultBox');
    box.classList.add('show');
    if (data.index >= 0) {
      box.innerHTML = `<span class="tag-found">✓ Found</span> — index <b>${data.index}</b>, value <b>${arr[data.index]}</b>, comparisons <b>${data.comparisons}</b>`;
    } else {
      box.innerHTML = `<span class="tag-miss">✗ Not found</span> — comparisons <b>${data.comparisons}</b>`;
    }
    const vis = document.getElementById('vis');
    vis.innerHTML = '';
    arr.forEach((v, i) => {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.textContent = v;
      if (data.steps && data.steps.some(s => s.pos === i)) cell.className += ' probe';
      if (i === data.index) cell.className += ' found';
      vis.appendChild(cell);
    });
  });
}

function runBenchmark() {
  document.getElementById('benchOutput').innerHTML = '<p class="loading">Running benchmark…</p>';
  fetch('/benchmark').then(r => r.json()).then(data => {
    const maxTime = Math.max(...data.map(r => Math.max(r.is_time, r.bs_time)));
    let html = '<table><thead><tr><th>Size</th><th class="is-col">IS Time (ms)</th><th class="bs-col">BS Time (ms)</th><th class="is-col">IS Comparisons</th><th class="bs-col">BS Comparisons</th></tr></thead><tbody>';
    data.forEach(r => {
      const isFasterTime = r.is_time < r.bs_time;
      const isFasterComp = r.is_comp < r.bs_comp;
      html += `<tr>
        <td>${r.size.toLocaleString()}</td>
        <td class="${isFasterTime ? 'faster' : 'is-col'}">${r.is_time}</td>
        <td class="${!isFasterTime ? 'faster' : 'bs-col'}">${r.bs_time}</td>
        <td class="${isFasterComp ? 'faster' : 'is-col'}">${r.is_comp}</td>
        <td class="${!isFasterComp ? 'faster' : 'bs-col'}">${r.bs_comp}</td>
      </tr>`;
    });
    html += '</tbody></table>';
    // bar chart for comparisons
    html += '<div style="margin-top:1.5rem"><div style="font-size:0.78rem;color:var(--muted);margin-bottom:0.8rem;font-family:JetBrains Mono,monospace;">COMPARISONS CHART</div>';
    const maxComp = Math.max(...data.map(r => r.bs_comp));
    data.forEach(r => {
      html += `<div style="margin-bottom:0.8rem">
        <div class="bar-label">${r.size.toLocaleString()}</div>
        <div class="bar-label" style="color:var(--accent)">IS</div>
        <div class="bar bar-is" style="width:${(r.is_comp/maxComp*100).toFixed(1)}%"></div>
        <div class="bar-label" style="color:var(--orange);margin-top:3px">BS</div>
        <div class="bar bar-bs" style="width:${(r.bs_comp/maxComp*100).toFixed(1)}%"></div>
      </div>`;
    });
    html += '</div>';
    document.getElementById('benchOutput').innerHTML = html;
  });
}
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    arr = sorted(data['arr'])
    target = data['target']
    idx, comps, steps = interpolation_search(arr, target)
    return jsonify({"index": idx, "comparisons": comps, "steps": steps})

@app.route('/benchmark')
def benchmark():
    return jsonify(performance_analysis())

if __name__ == '__main__':
    app.run(debug=True)