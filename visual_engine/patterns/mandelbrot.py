import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import FloatSlider, IntSlider
from engines.renderer import BasePattern

class Mandelbrot(BasePattern):
    def get_controls(self):
        return [
            FloatSlider(value=1.0, min=0.1, max=100.0, step=0.1, description='Zoom:'),
            FloatSlider(value=-0.5, min=-2.0, max=1.0, step=0.01, description='Center X:'),
            FloatSlider(value=0.0, min=-1.5, max=1.5, step=0.01, description='Center Y:'),
            IntSlider(value=100, min=10, max=1000, step=10, description='Max Iter:')
        ]

    def render(self, zoom=1.0, center_x=-0.5, center_y=0.0, max_iter=100):
        width, height = 800, 800
        x_min, x_max = center_x - 1.5/zoom, center_x + 1.5/zoom
        y_min, y_max = center_y - 1.5/zoom, center_y + 1.5/zoom
        
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.full(C.shape, True, dtype=bool)
        N = np.zeros(C.shape, dtype=int)
        
        for i in range(max_iter):
            mask = M & (np.abs(Z) <= 2)
            if not np.any(mask):
                break
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            N[mask] = i
            M[np.abs(Z) > 2] = False
            
        plt.figure(figsize=(10, 10))
        plt.imshow(N, extent=(x_min, x_max, y_min, y_max), cmap='magma')
        plt.colorbar(label='Iterations')
        plt.title(f"Mandelbrot Set (zoom={zoom}, iter={max_iter})")
        plt.axis('off')
        plt.show()
