# daa5 — Min/Max Divide & Conquer

Compares a divide-and-conquer min/max algorithm (~3n/2 - 2 comparisons)
against a naive linear scan (~2n comparisons), with a small Flask front end.

## Files
- `minmax.py` — the algorithm + naive comparison + demo logic (no I/O side effects, safe to import)
- `app.py` — Flask web app that renders results in the browser
- `templates/index.html` — results page
- `requirements.txt` — dependencies
- `render.yaml` — Render blueprint (optional, for one-click deploy)

## Run locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

To just run the plain console script (no web server):

```bash
python minmax.py
```

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: min/max divide and conquer + Flask app"
git branch -M main
git remote add origin https://github.com/<your-username>/daa5.git
git push -u origin main
```

## Deploy to Render

**Option A — Dashboard**
1. Push this repo to GitHub (above).
2. Go to https://dashboard.render.com → **New** → **Web Service**.
3. Connect your GitHub repo.
4. Settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**. Render will build and give you a public URL.

**Option B — Blueprint (render.yaml)**
1. Push this repo to GitHub.
2. In Render, choose **New** → **Blueprint**, point it at the repo.
3. Render reads `render.yaml` and provisions the service automatically.
