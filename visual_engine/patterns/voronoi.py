import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import IntSlider
from engines.renderer import BasePattern
from scipy.spatial import Voronoi, voronoi_plot_2d

class VoronoiDiagram(BasePattern):
    def get_controls(self):
        return [
            IntSlider(value=20, min=5, max=100, step=5, description='Points:')
        ]

    def render(self, num_points=20):
        points = np.random.rand(num_points, 2)
        vor = Voronoi(points)
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black', line_width=1, line_alpha=0.6, point_size=2)
        
        # Color the regions
        for region_index in vor.point_region:
            region = vor.regions[region_index]
            if not -1 in region and len(region) > 0:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon), alpha=0.4)
                
        plt.title(f"Voronoi Diagram ({num_points} points)")
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
        plt.show()
