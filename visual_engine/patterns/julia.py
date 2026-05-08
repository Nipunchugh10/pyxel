import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import FloatSlider, IntSlider
from engines.renderer import BasePattern

class JuliaSet(BasePattern):
    def get_controls(self):
        return [
            FloatSlider(value=-0.7, min=-2.0, max=2.0, step=0.01, description='C Real:'),
            FloatSlider(value=0.27, min=-2.0, max=2.0, step=0.01, description='C Imag:'),
            IntSlider(value=100, min=10, max=1000, step=10, description='Max Iter:'),
            FloatSlider(value=1.0, min=0.1, max=10.0, step=0.1, description='Zoom:')
        ]

    def render(self, c_real=-0.7, c_imag=0.27, max_iter=100, zoom=1.0):
        width, height = 800, 800
        x_min, x_max = -1.5/zoom, 1.5/zoom
        y_min, y_max = -1.5/zoom, 1.5/zoom
        
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        C = complex(c_real, c_imag)
        M = np.full(Z.shape, True, dtype=bool)
        N = np.zeros(Z.shape, dtype=int)
        
        for i in range(max_iter):
            mask = M & (np.abs(Z) <= 2)
            if not np.any(mask):
                break
            Z[mask] = Z[mask] * Z[mask] + C
            N[mask] = i
            M[np.abs(Z) > 2] = False
            
        plt.figure(figsize=(10, 10))
        plt.imshow(N, extent=(x_min, x_max, y_min, y_max), cmap='twilight')
        plt.colorbar(label='Iterations')
        plt.title(f"Julia Set (c={C}, zoom={zoom})")
        plt.axis('off')
        plt.show()
