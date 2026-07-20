import os
import time

from flask import Flask, render_template, request

from n_queens import solve_n_queens

app = Flask(__name__)

MAX_N = 12  # guard against huge N freezing the free web dyno


@app.route("/", methods=["GET"])
def index():
    n = request.args.get("n", default=4, type=int)
    error = None
    solutions, backtracks, elapsed = [], 0, 0.0

    if n is None or n < 1:
        error = "Please enter a positive integer for N."
    elif n > MAX_N:
        error = f"For this demo, N is capped at {MAX_N} to keep response times reasonable."
    else:
        start = time.perf_counter()
        solutions, backtracks = solve_n_queens(n)
        elapsed = time.perf_counter() - start

    return render_template(
        "index.html",
        n=n,
        error=error,
        solutions=solutions,
        backtracks=backtracks,
        elapsed=elapsed,
        solution_count=len(solutions),
        max_n=MAX_N,
    )


if __name__ == "__main__":
    # Render sets $PORT; default to 5000 for local runs.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
