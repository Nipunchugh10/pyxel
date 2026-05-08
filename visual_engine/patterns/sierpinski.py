import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import IntSlider
from engines.renderer import BasePattern

class SierpinskiTriangle(BasePattern):
    def get_controls(self):
        return [
            IntSlider(value=1000, min=100, max=10000, step=100, description='Iterations:')
        ]

    def render(self, iterations=1000):
        vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
        points = [np.array([0.5, 0.5])]
        
        for _ in range(iterations):
            target = vertices[np.random.randint(3)]
            points.append((points[-1] + target) / 2)
            
        points = np.array(points)
        plt.figure(figsize=(10, 10))
        plt.scatter(points[:, 0], points[:, 1], s=1, c='blue', alpha=0.5)
        plt.title(f"Sierpinski Triangle (Chaos Game, {iterations} points)")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
