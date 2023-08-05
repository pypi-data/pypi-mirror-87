""" This module provides a support material class.
"""

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


class Support:
    def __init__(self, ax, pos, color):
        self._ax = ax
        self._pos = pos
        self._color = color
        self._isSupport = True
        self.faces = None

    @property
    def pos(self):
        return self._pos

    @property
    def color(self):
        return self._color

    @property
    def isSupport(self):
        return self._isSupport

    def draw(self):
        (x, y, z) = self._pos
        points = self.generate_support_def(x, y, z)

        points = np.array(points)

        edges = [
            [points[0], points[1], points[3]],
            [points[0], points[2], points[3]],
            [points[1], points[4], points[3]],
            [points[2], points[4], points[3]],
            [points[0], points[1], points[2], points[4]]
        ]

        self.faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
        self.faces.set_facecolor(self._color)

        self._ax.add_collection3d(self.faces)

        # Plot the points themselves to force the scaling of the axes
        self._ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=0)

    def remove(self):
        self.faces.set_facecolor((0, 0, 0, 0))
        self.faces.set_edgecolor((0, 0, 0, 0))

    def generate_support_def(self, x, y, z):
        return [(x, y, z), (x, y + 1, z), (x + 1, y, z), (x+.5, y+.5, z + 1), (x+1, y+1, z)]
