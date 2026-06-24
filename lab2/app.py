from flask import Flask, render_template_string, request, jsonify
import time
import random

app = Flask(__name__)

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1; j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons

def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)
    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q
    return matches, comparisons

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ex. 02 — String Matching</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --accent: #58a6ff; --green: #3fb950; --orange: #f0883e;
    --purple: #bc8cff; --text: #e6edf3; --muted: #8b949e; --danger: #f85149;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; min-height: 100vh; }
  header { border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; display: flex; align-items: center; gap: 1rem; }
  .badge { background: var(--purple); color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 4px; }
  header h1 { font-size: 1.1rem; font-weight: 600; }
  header p { font-size: 0.8rem; color: var(--muted); margin-top: 0.15rem; }
  main { max-width: 1000px; margin: 0 auto; padding: 2rem; }
  section { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }
  section h2 { font-size: 0.85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1.2rem; }
  .row { display: flex; gap: 1rem; flex-wrap: wrap; }
  .field { flex: 1; min-width: 200px; }
  label { display: block; font-size: 0.8rem; color: var(--muted); margin-bottom: 0.4rem; font-family: 'JetBrains Mono', monospace; }
  input, textarea { width: 100%; background: var(--bg); border: 1px solid var(--border); color: var(--text); padding: 0.6rem 0.8rem; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; outline: none; transition: border-color 0.2s; resize: vertical; }
  input:focus, textarea:focus { border-color: var(--purple); }
  .btn { background: var(--purple); color: #000; border: none; padding: 0.65rem 1.4rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: opacity 0.2s; }
  .btn:hover { opacity: 0.85; }
  .btn-outline { background: transparent; color: var(--purple); border: 1px solid var(--purple); }
  .gap { margin-top: 0.8rem; }
  .algo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem; }
  .algo-card { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }
  .algo-card h3 { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.8rem; font-family: 'JetBrains Mono', monospace; }
  .algo-card.naive h3 { color: var(--orange); }
  .algo-card.kmp h3 { color: var(--accent); }
  .algo-card.rk h3 { color: var(--green); }
  .stat-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-bottom: 0.4rem; }
  .stat-row span:first-child { color: var(--muted); }
  .highlight-text { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; line-height: 1.8; word-break: break-all; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; margin-top: 1rem; max-height: 160px; overflow-y: auto; }
  .hl { background: var(--purple); color: #000; border-radius: 2px; padding: 0 1px; font-weight: 700; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); color: var(--muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace; }
  td { padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; }
  tr:last-child td { border-bottom: none; }
  .naive-col { color: var(--orange); } .kmp-col { color: var(--accent); } .rk-col { color: var(--green); }
  .best { font-weight: 700; } 
  .loading { color: var(--muted); font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }
  .bar-wrap { margin-top: 1.2rem; }
  .bar-row { margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.6rem; }
  .bar-name { font-size: 0.75rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; width: 90px; text-align: right; flex-shrink: 0; }
  .bar { height: 14px; border-radius: 3px; transition: width 0.6s ease; min-width: 2px; }
  .bar-naive { background: var(--orange); }
  .bar-kmp { background: var(--accent); }
  .bar-rk { background: var(--green); }
  .bar-val { font-size: 0.72rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
  .matches-badge { display: inline-block; background: var(--purple); color: #000; border-radius: 999px; font-size: 0.72rem; font-weight: 700; padding: 1px 8px; font-family: 'JetBrains Mono', monospace; }
  .algo-tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }
  .tab { padding: 0.4rem 0.9rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; cursor: pointer; background: var(--bg); color: var(--muted); transition: all 0.2s; }
  .tab.active { border-color: var(--purple); color: var(--purple); }
  @media(max-width:640px) { .algo-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <div><div class="badge">EX. 02</div></div>
  <div>
    <h1>String Matching Algorithms</h1>
    <p>Naive · Rabin-Karp · KMP — CS5303 DAA Lab</p>
  </div>
</header>
<main>
  <section>
    <h2>Live Pattern Search</h2>
    <div class="row">
      <div class="field">
        <label>Text</label>
        <textarea id="textInput" rows="2">AABAACAADAABAABA</textarea>
      </div>
      <div class="field" style="max-width:220px">
        <label>Pattern</label>
        <input id="patternInput" value="AABA">
      </div>
    </div>
    <div class="gap">
      <button class="btn" onclick="runSearch()">Search</button>
    </div>
    <div id="algoResults" style="display:none">
      <div class="algo-grid" id="cardsGrid"></div>
      <div id="highlightBox" class="highlight-text" style="margin-top:1rem;display:none"></div>
    </div>
  </section>

  <section>
    <h2>Performance Benchmark</h2>
    <p style="font-size:0.82rem;color:var(--muted);margin-bottom:1rem;">10,000-character random text. Patterns of increasing length tested across all three algorithms.</p>
    <button class="btn btn-outline" onclick="runBenchmark()">Run Benchmark</button>
    <div id="benchOutput" style="margin-top:1.2rem;"></div>
  </section>
</main>
<script>
function runSearch() {
  const text = document.getElementById('textInput').value;
  const pattern = document.getElementById('patternInput').value;
  if (!text || !pattern) return;
  fetch('/search', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({text, pattern})
  }).then(r => r.json()).then(data => {
    document.getElementById('algoResults').style.display = 'block';
    const algos = [
      {key:'naive', label:'Naive', cls:'naive', col:'var(--orange)'},
      {key:'kmp',   label:'KMP',   cls:'kmp',   col:'var(--accent)'},
      {key:'rk',    label:'Rabin-Karp', cls:'rk', col:'var(--green)'}
    ];
    const minComp = Math.min(data.naive.comparisons, data.kmp.comparisons, data.rk.comparisons);
    let cards = '';
    algos.forEach(a => {
      const d = data[a.key];
      const best = d.comparisons === minComp;
      cards += `<div class="algo-card ${a.cls}">
        <h3>${a.label}${best ? ' ★' : ''}</h3>
        <div class="stat-row"><span>Comparisons</span><span style="color:${a.col};font-weight:${best?700:400}">${d.comparisons}</span></div>
        <div class="stat-row"><span>Matches</span><span><span class="matches-badge">${d.matches.length}</span></span></div>
        <div class="stat-row"><span>Positions</span><span style="color:var(--text)">[${d.matches.join(', ')}]</span></div>
      </div>`;
    });
    document.getElementById('cardsGrid').innerHTML = cards;
    // highlight
    const box = document.getElementById('highlightBox');
    box.style.display = 'block';
    const matches = data.naive.matches;
    let out = '';
    let i = 0;
    const m = pattern.length;
    const matchSet = new Set(matches);
    while (i < text.length) {
      if (matchSet.has(i)) {
        out += `<span class="hl">${escHtml(text.slice(i, i+m))}</span>`;
        i += m;
      } else {
        out += escHtml(text[i]);
        i++;
      }
    }
    box.innerHTML = out;
  });
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function runBenchmark() {
  document.getElementById('benchOutput').innerHTML = '<p class="loading">Running benchmark…</p>';
  fetch('/benchmark').then(r => r.json()).then(data => {
    const maxComp = Math.max(...data.map(r => Math.max(r.naive, r.kmp, r.rk)));
    let html = '<table><thead><tr><th>Pattern</th><th class="naive-col">Naive</th><th class="kmp-col">KMP</th><th class="rk-col">Rabin-Karp</th><th>Winner</th></tr></thead><tbody>';
    data.forEach(r => {
      const min = Math.min(r.naive, r.kmp, r.rk);
      const winner = r.naive === min ? '<span class="naive-col">Naive</span>' : r.kmp === min ? '<span class="kmp-col">KMP</span>' : '<span class="rk-col">Rabin-Karp</span>';
      html += `<tr>
        <td>${r.pattern}</td>
        <td class="${r.naive===min?'best naive-col':'naive-col'}">${r.naive.toLocaleString()}</td>
        <td class="${r.kmp===min?'best kmp-col':'kmp-col'}">${r.kmp.toLocaleString()}</td>
        <td class="${r.rk===min?'best rk-col':'rk-col'}">${r.rk.toLocaleString()}</td>
        <td>${winner}</td>
      </tr>`;
    });
    html += '</tbody></table>';
    // bar chart
    html += '<div class="bar-wrap"><div style="font-size:0.78rem;color:var(--muted);font-family:JetBrains Mono,monospace;margin-bottom:0.8rem;">COMPARISON COUNT BY PATTERN</div>';
    data.forEach(r => {
      html += `<div style="margin-bottom:1rem"><div style="font-size:0.75rem;color:var(--muted);font-family:JetBrains Mono,monospace;margin-bottom:4px">Pattern: "${r.pattern}"</div>
        <div class="bar-row"><div class="bar-name">Naive</div><div class="bar bar-naive" style="width:${(r.naive/maxComp*300).toFixed(0)}px"></div><div class="bar-val">${r.naive.toLocaleString()}</div></div>
        <div class="bar-row"><div class="bar-name">KMP</div><div class="bar bar-kmp" style="width:${(r.kmp/maxComp*300).toFixed(0)}px"></div><div class="bar-val">${r.kmp.toLocaleString()}</div></div>
        <div class="bar-row"><div class="bar-name">Rabin-Karp</div><div class="bar bar-rk" style="width:${(r.rk/maxComp*300).toFixed(0)}px"></div><div class="bar-val">${r.rk.toLocaleString()}</div></div>
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
    text = data['text']
    pattern = data['pattern']
    m1, c1 = naive_search(text, pattern)
    m2, c2 = kmp_search(text, pattern)
    m3, c3 = rabin_karp(text, pattern)
    return jsonify({
        "naive": {"matches": m1, "comparisons": c1},
        "kmp":   {"matches": m2, "comparisons": c2},
        "rk":    {"matches": m3, "comparisons": c3},
    })

@app.route('/benchmark')
def benchmark():
    text_large = ''.join(random.choices('ABCD', k=10000))
    patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']
    results = []
    for p in patterns:
        _, c1 = naive_search(text_large, p)
        _, c2 = kmp_search(text_large, p)
        _, c3 = rabin_karp(text_large, p)
        results.append({"pattern": p, "naive": c1, "kmp": c2, "rk": c3})
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)