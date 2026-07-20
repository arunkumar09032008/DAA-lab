# N-Queens Solver (Backtracking)

A Flask web app that solves the N-Queens problem using backtracking and
displays every solution as a chessboard, along with the solution count
and number of backtracking attempts.

## Files
- `n_queens.py` – the core backtracking algorithm (also runnable standalone
  from the command line: `python n_queens.py`)
- `app.py` – Flask web app that wraps the algorithm
- `templates/index.html` – web page that renders the boards
- `requirements.txt` – Python dependencies
- `render.yaml` – Render deployment config
- `.gitignore`

## Run locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

## Push to GitHub

```bash
cd n_queens
git init
git add .
git commit -m "N-Queens backtracking solver with Flask web UI"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(Create the empty repo on GitHub first, at https://github.com/new — don't
initialize it with a README there, since you already have one locally.)

## Deploy on Render

1. Push the code to GitHub (above).
2. Go to https://dashboard.render.com and click **New +** → **Web Service**.
3. Connect your GitHub account and select this repository.
4. Render should auto-detect `render.yaml` and pre-fill the settings. If not,
   set them manually:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Create Web Service**. Render will build and deploy; you'll get a
   public URL like `https://n-queens-solver.onrender.com`.

Note: the free Render plan spins down after inactivity, so the first request
after idle time can take ~30-60 seconds to wake up.
