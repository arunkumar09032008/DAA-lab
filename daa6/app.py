import os
from flask import Flask, request, jsonify, render_template

from daa6 import solve

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/solve', methods=['POST'])
def api_solve():
    payload = request.get_json(force=True, silent=True) or {}
    dims_raw = payload.get('dims')

    if not dims_raw:
        return jsonify({'error': 'Provide "dims" as a list of integers, e.g. [10, 30, 5, 60, 10]'}), 400

    try:
        dims = [int(d) for d in dims_raw]
    except (TypeError, ValueError):
        return jsonify({'error': 'All dimensions must be integers'}), 400

    if len(dims) < 2:
        return jsonify({'error': 'Provide at least 2 dimensions (1 matrix)'}), 400

    if any(d <= 0 for d in dims):
        return jsonify({'error': 'All dimensions must be positive integers'}), 400

    result = solve(dims)

    matrices = [{'name': f'A{i + 1}', 'rows': dims[i], 'cols': dims[i + 1]}
                for i in range(result['n'])]

    return jsonify({
        'matrices': matrices,
        'min_multiplications': result['min_multiplications'],
        'optimal_parenthesization': result['optimal_parenthesization'],
    })


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
