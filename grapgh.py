from flask import Flask, request, jsonify
from sympy import symbols, lambdify, sympify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/generate_graph')
def generate_graph():
    expression = request.args.get('expression')
    if not expression:
        return jsonify({'error': 'No expression provided'}), 400

    try:
        x = symbols('x')
        expr = sympify(expression)
        f = lambdify(x, expr, 'numpy')

        x_values = np.linspace(-10, 10, 400)
        y_values = f(x_values)

        return jsonify({
            'xValues': x_values.tolist(),
            'yValues': y_values.tolist()
        })
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

@app.route('/plot_graph')
def plot_graph():
    expression = request.args.get('expression')
    if not expression:
        return jsonify({'error': 'No expression provided'}), 400

    try:
        x = symbols('x')
        expr = sympify(expression)
        f = lambdify(x, expr, 'numpy')

        x_values = np.linspace(-10, 10, 400)
        y_values = f(x_values)

        plt.figure()
        plt.plot(x_values, y_values)
        plt.title(f'Graph of {expression}')
        plt.xlabel('x')
        plt.ylabel('f(x)')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return f'<img src="data:image/png;base64,{plot_url}"/>'
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
