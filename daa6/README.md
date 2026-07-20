# Matrix Chain Multiplication Solver

A dynamic programming solution to the Matrix Chain Multiplication problem,
wrapped in a small Flask web app.

- `daa6.py` — the core algorithm. Runs standalone: `python3 daa6.py`
- `app.py` — Flask web app that serves a UI and a JSON API
- `templates/index.html` — front-end
- `requirements.txt` — Python dependencies
- `render.yaml` — Render deployment config

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Visit http://localhost:5000

Or just run the algorithm from the command line, no Flask needed:

```bash
python3 daa6.py
```

## API

`POST /api/solve`

```json
{ "dims": [10, 30, 5, 60, 10] }
```

Response:

```json
{
  "matrices": [...],
  "min_multiplications": 5000,
  "optimal_parenthesization": "((A1 x A2) x (A3 x A4))"
}
```

## Push to GitHub

```bash
cd matrix-chain-app
git init
git add .
git commit -m "Matrix chain multiplication solver"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(Create the empty repo on GitHub first at https://github.com/new — don't
initialize it with a README so there's no merge conflict.)

## Deploy to Render

**Option A — Dashboard (easiest)**
1. Push this repo to GitHub (steps above).
2. Go to https://dashboard.render.com → **New** → **Web Service**.
3. Connect your GitHub repo.
4. Render will detect `render.yaml` automatically and configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Click **Create Web Service**. Your app will be live at
   `https://<service-name>.onrender.com` in a couple of minutes.

**Option B — render.yaml (Blueprint)**
1. Push to GitHub.
2. In Render dashboard: **New** → **Blueprint** → select your repo.
3. Render reads `render.yaml` and provisions the service for you.

On Render's free plan the service spins down after inactivity and takes a
few seconds to wake up on the next request — that's normal.
