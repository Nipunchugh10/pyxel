import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import IntSlider
from engines.renderer import BasePattern

class PenroseTiling(BasePattern):
    def get_controls(self):
        return [
            IntSlider(value=4, min=0, max=8, description='Generations:')
        ]

    def render(self, generations=4):
        phi = (1 + np.sqrt(5)) / 2

        def subdivide(triangles):
            result = []
            for type, A, B, C in triangles:
                if type == 0:
                    # Thin triangle
                    P = A + (B - A) / phi
                    result += [(0, C, P, B), (1, P, C, A)]
                else:
                    # Thick triangle
                    Q = B + (A - B) / phi
                    R = B + (C - B) / phi
                    result += [(1, R, Q, B), (0, Q, R, A), (1, C, A, Q)]
            return result

        triangles = []
        for i in range(10):
            B = np.exp(1j * (2*i - 1) * np.pi / 10)
            C = np.exp(1j * (2*i + 1) * np.pi / 10)
            if i % 2 == 0:
                triangles.append((0, 0j, B, C))
            else:
                triangles.append((0, 0j, C, B))

        for _ in range(generations):
            triangles = subdivide(triangles)

        plt.figure(figsize=(10, 10))
        for type, A, B, C in triangles:
            pts = np.array([[A.real, A.imag], [B.real, B.imag], [C.real, C.imag]])
            poly = plt.Polygon(pts, facecolor='orange' if type == 0 else 'blue', edgecolor='white', linewidth=0.1)
            plt.gca().add_patch(poly)

        plt.axis('equal')
        plt.axis('off')
        plt.title(f"Penrose Tiling (Gens={generations})")
        plt.show()
