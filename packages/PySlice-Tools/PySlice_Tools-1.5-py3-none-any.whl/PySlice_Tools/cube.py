""" This module provides a cube class.
"""

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


class Cube:
    def __init__(self, ax, pos, color):
        self._ax = ax
        self._pos = pos
        self._color = color
        self._isSupport = False
        self._faces = None

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
        cube_definition = self.generate_cube_def(x, y, z)

        # https://stackoverflow.com/questions/44881885/python-draw-parallelepiped
        cube_definition_array = [
            np.array(list(item))
            for item in cube_definition
        ]

        points = []
        points += cube_definition_array
        vectors = [
            cube_definition_array[1] - cube_definition_array[0],
            cube_definition_array[2] - cube_definition_array[0],
            cube_definition_array[3] - cube_definition_array[0]
        ]

        points += [cube_definition_array[0] + vectors[0] + vectors[1]]
        points += [cube_definition_array[0] + vectors[0] + vectors[2]]
        points += [cube_definition_array[0] + vectors[1] + vectors[2]]
        points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

        points = np.array(points)

        edges = [
            [points[0], points[3], points[5], points[1]],
            [points[1], points[5], points[7], points[4]],
            [points[4], points[2], points[6], points[7]],
            [points[2], points[6], points[3], points[0]],
            [points[0], points[2], points[4], points[1]],
            [points[3], points[6], points[7], points[5]]
        ]

        self._faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
        self._faces.set_facecolor(self._color)

        self._ax.add_collection3d(self._faces)

    def remove(self):
        self._faces.remove()

    def generate_cube_def(self, x, y, z):
        return [(x, y, z), (x, y + 1, z), (x + 1, y, z), (x, y, z + 1)]


class CubeSet:
    """
    Add a cube set given x, y, z position as a tuple,
    sx, sy, sz as a tuple of the cube dimension.
    Return -1 if a cube at position already exists and 1 otherwise.
    """
    def __init__(self, ax, pos, dim, color):
        self._ax = ax
        self._pos = pos
        self._dim = dim
        self._color = color
        self._faces = None
        self._isSupport = False
        self._edges = []
        self.initialize_edges()

    @property
    def dim(self):
        return self._dim

    @property
    def isSupport(self):
        return self._isSupport

    @property
    def pos(self):
        return self._pos

    @property
    def color(self):
        return self._color

    def initialize_edges(self):
        (x, y, z) = self._pos
        (sx, sy, sz) = self._dim

        # 2 sides along x axis
        for j in range(y, y + sy):
            for k in range(z, z + sz):
                self._edges.append([[x, j, k], [x, j, k + 1], [x, j + 1, k + 1], [x, j + 1, k]])
                self._edges.append([[x + sx, j, k], [x + sx, j, k + 1],
                                    [x + sx, j + 1, k + 1], [x + sx, j + 1, k]])

        # 2 sides along y axis
        for i in range(x, x + sx):
            for k in range(z, z + sz):
                self._edges.append([[i, y, k], [i, y, k + 1], [i + 1, y, k + 1], [i + 1, y, k]])
                self._edges.append([[i, y + sy, k], [i, y + sy, k + 1],
                                    [i + 1, y + sy, k + 1], [i + 1, y + sy, k]])

        # 2 sides along z axis
        for i in range(x, x + sx):
            for j in range(y, y + sy):
                self._edges.append([[i, j, z], [i, j + 1, z], [i + 1, j + 1, z], [i + 1, j, z]])
                self._edges.append([[i, j, z + sz], [i, j + 1, z + sz],
                                    [i + 1, j + 1, z + sz], [i + 1, j, z + sz]])

    def draw(self):
        self._faces = Poly3DCollection(np.array(self._edges), linewidths=1, edgecolors='k')
        self._faces.set_facecolor(self._color)

        self._ax.add_collection3d(self._faces)

    def remove(self):
        self._faces.remove()

    def remove_cube(self, pos):
        # Position of cube to be deleted
        (xx, yy, zz) = pos

        # 6 sides of the cube
        surface1 = [[xx, yy, zz], [xx, yy, zz + 1], [xx, yy + 1, zz + 1], [xx, yy + 1, zz]]
        surface2 = [[xx, yy, zz], [xx, yy, zz + 1], [xx + 1, yy, zz + 1], [xx + 1, yy, zz]]
        surface3 = [[xx, yy, zz], [xx, yy + 1, zz], [xx + 1, yy + 1, zz], [xx + 1, yy, zz]]
        surface4 = [[i + 1, j, k] for [i, j, k] in surface1]
        surface5 = [[i, j + 1, k] for [i, j, k] in surface2]
        surface6 = [[i, j, k + 1] for [i, j, k] in surface3]
        surfaces = [surface1, surface2, surface3, surface4, surface5, surface6]

        # Invert sides.
        for surface in surfaces:
            if surface in self._edges:
                self._edges.remove(surface)
            else:
                self._edges.append(surface)

        self._faces.remove()
        if self._edges:
            self.draw()

