import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def generate_graph(equation_str, x_range=(-10, 10), num_points=1000):
    """
    Generate a graph for a given equation using Matplotlib.
    :param equation_str: The equation as a string (e.g., "x**2 + 3*x + 2").
    :param x_range: Tuple (min, max) for the x-axis range.
    :param num_points: Number of points to plot.
    :return: Base64-encoded image of the graph.
    """
    try:
        # Parse the equation using SymPy
        x = symbols('x')
        equation = sympify(equation_str)
        func = lambdify(x, equation, modules=['numpy'])

        # Generate x and y values
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = func(x_vals)

        # Create the plot
        plt.figure()
        plt.plot(x_vals, y_vals, label=f"y = {equation_str}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"Graph of y = {equation_str}")
        plt.grid(True)
        plt.legend()

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Encode the image as base64
        graph_image = base64.b64encode(buf.read()).decode('utf-8')
        return graph_image
    except Exception as e:
        logging.error(f"Error generating graph: {e}")
        return None