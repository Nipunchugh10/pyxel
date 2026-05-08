import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import IntSlider
from engines.renderer import BasePattern

class KochSnowflake(BasePattern):
    def get_controls(self):
        return [
            IntSlider(value=3, min=0, max=6, description='Depth:')
        ]

    def render(self, depth=3):
        def get_koch_points(p1, p2, depth):
            if depth == 0:
                return [p1, p2]
            
            p1 = np.array(p1)
            p2 = np.array(p2)
            
            v = p2 - p1
            s1 = p1 + v / 3
            s3 = p1 + 2 * v / 3
            
            # Rotate v/3 by 60 degrees
            angle = np.pi / 3
            rot = np.array([[np.cos(angle), -np.sin(angle)], 
                            [np.sin(angle),  np.cos(angle)]])
            s2 = s1 + rot @ (v / 3)
            
            points = []
            points.extend(get_koch_points(p1, s1, depth - 1)[:-1])
            points.extend(get_koch_points(s1, s2, depth - 1)[:-1])
            points.extend(get_koch_points(s2, s3, depth - 1)[:-1])
            points.extend(get_koch_points(s3, p2, depth - 1))
            return points

        v1 = np.array([0, 0])
        v2 = np.array([1, 0])
        v3 = np.array([0.5, -np.sqrt(3)/2])
        
        points = []
        points.extend(get_koch_points(v1, v2, depth)[:-1])
        points.extend(get_koch_points(v2, v3, depth)[:-1])
        points.extend(get_koch_points(v3, v1, depth))
        
        points = np.array(points)
        plt.figure(figsize=(10, 10))
        plt.plot(points[:, 0], points[:, 1], 'b-')
        plt.title(f"Koch Snowflake (depth={depth})")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
