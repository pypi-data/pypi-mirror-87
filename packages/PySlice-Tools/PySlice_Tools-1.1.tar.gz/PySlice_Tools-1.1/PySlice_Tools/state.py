""" This module provides a class to keep track of the internal state
of the application.
"""
import os.path
import PySlice_Tools.slice._slice
import json
import numpy as np

from PySlice_Tools.support import Support
from PySlice_Tools.cube import Cube, CubeSet


class State:
    def __init__(self, canvas, ax):
        self._canvas = canvas
        self._ax = ax
        self._cube_map = dict()
        self._command_list = []
        self._command_index = 0
        self._command_options = ['addcube', 'delcube', 'save', 'load', 'clear', 'delcubeset', 'addcubeset', 'addmodel',
                                 'submodel', 'help', 'slice', 'setbound', 'undo', 'redo', 'move', 'flip', 'rotate','addsupport','slicerprop']  # Used for tab autocomplete
        self._undo_stack = []
        self._redo_stack = []
        self._color = (0, .7, 1, .8)  # Default normalized RGBA cube color
        self._bound = None
        self._bound1 = None
        self._bound2 = None
        self._bound3 = None

        self._support_color = (.6, .6, .6, .5)    #Default RGBA support color
        self._slicerprop = [100, 100, 1500, 1.0, 1.0, 0.5] #initpos{x, y}, speed, extrustionConst, infillConst, layerHeight

    def add_cube(self, pos, color=None):
        """
        Add a unit cube given x, y, z position as a tuple.
        Return -1 if cube already exists and 1 otherwise.
        """
        # If a cube is already added at the position given,
        # don't do anything
        if self.has_cube(pos):
            print('A cube has already been added at the given position', flush=True)
            return -1, 'A cube has already been added at ' + str(pos)

        if self._bound and not self.is_within_bound(pos, (1, 1, 1)):
            return -1, 'Cube not added because it is out of bound.'

        # Update color.
        if color:
            self._color = color

        # resize grid
        self.resize_grid(pos)

        # Draw cube on canvas
        cube = Cube(self._ax, pos, self._color)
        cube.draw()

        self._canvas.draw()

        # Add cube to internal map
        self._cube_map[pos] = cube

        return 1, ''

    def delete(self, pos):
        """
        Deletes an object given x, y, z position as a tuple.
        Return -1 if cube deletion not successful and 1 if successful.
        """
        if not self.has_cube(pos):
            print('Object does not exist', flush=True)
            return -1

        # Remove cube from canvas by setting it to transparent
        cube = self._cube_map[pos]
        cube.remove()
        self._canvas.draw()

        # Remove cube from internal map
        del self._cube_map[pos]

        return 1

    def is_within_bound(self, pos, dim):
        # position of the opposing corner
        pos1 = (pos[0] + dim[0], pos[1] + dim[1], pos[2] + dim[2])

        # boundary: (min_x, min_y, min_z, max_x, max_y, max_z)
        if self._bound[0] <= pos[0] <= self._bound[3] and self._bound[1] <= pos[1] <= self._bound[4] and \
                self._bound[2] <= pos[2] <= self._bound[5] and self._bound[0] <= pos1[0] <= self._bound[3] \
                and self._bound[1] <= pos1[1] <= self._bound[4] and self._bound[2] <= pos1[2] <= self._bound[5]:
            return True
        return False

    def resize_grid(self, pos):
        # resize grid if new cube is out of axis limit
        low = min(pos)
        low = min(low, self._ax.get_xlim()[0])
        high = max(pos)
        high = max(high, self._ax.get_xlim()[1])
        self._ax.set_xlim(low, high, 1)
        self._ax.set_ylim(low, high, 1)
        self._ax.set_zlim(low, high, 1)

    def has_cube(self, pos):
        return pos in self._cube_map

    def is_cube(self, pos):
        return isinstance(self._cube_map[pos], Cube)

    def is_cubeset(self, pos):
        return isinstance(self._cube_map[pos], CubeSet)

    def get_cube_list(self):
        return list(self._cube_map.keys())

    def get_possible_commands(self):
        return self._command_options

    # Default directory is cwd if no dir passed in
    def save_cubes_to_file(self, filename, directory='./'):
        with open(os.path.join(directory, filename + '.slice'), 'w+') as f:
            for pos in self.get_cube_list():
                color = self._cube_map[pos]._color
                f.write(str(pos[0]) + ' ' + 
                        str(pos[1]) + ' ' + 
                        str(pos[2]) + ' ' + 
                        str(color[0]) + ' ' +   # Cube color tuple in the form (R, G, B, transparency)
                        str(color[1]) + ' ' +
                        str(color[2]) + ' ' +
                        str(color[3]))
                if(self._cube_map[pos].isSupport):
                    f.write(" s")
                f.write("\n");

    def clear(self):  # clear clears all of the cubes from the display
        # re-draw canvas
        self._ax.clear()

        if self._bound:
            self.set_bound(self._bound)
        else:
            self._ax.set_xlim(0, 5, 1)
            self._ax.set_ylim(0, 5, 1)
            self._ax.set_zlim(0, 5, 1)
            self._ax.set_xlabel('X')
            self._ax.set_ylabel('Y')
            self._ax.set_zlabel('Z')
            self._canvas.draw()

        self._cube_map.clear()

    def load_cube(self, pos, color):
        """
        Load a unit cube without updating the canvas.
        """
        self._color = color

        # resize grid
        self.resize_grid(pos)

        # Draw cube on canvas
        cube = Cube(self._ax, pos, self._color)
        cube.draw()

        # Add cube to internal map
        self._cube_map[pos] = cube

    def load_cubes_to_file(self, directory, clear=True, offset=(
            0, 0, 0)):  # clear is an optional paramater. Set to true by default.  Offset is optional
        try:
            with open(directory, "r") as file:
                if clear:
                    self.clear()
                for cube in file:
                    cube_stats = cube.split(' ')
                    pos = (int(cube_stats[0]) + offset[0], int(cube_stats[1]
                                                               ) + offset[1], int(cube_stats[2]) + offset[2])
                    r = float(cube_stats[3])
                    g = float(cube_stats[4])
                    b = float(cube_stats[5])
                    a = float(cube_stats[6].rstrip('\n'))
                    if(cube[-2] == 's'):
                        self.add_support(pos)
                    else:
                        self.load_cube(pos, (r, g, b, a))

                self._canvas.draw()
        except Exception as err:
            print(err)
            return -1, str(err)

        return 1, ''

    def get_current_color(self):
        return self._color

    def save_command(self, command):
        self._command_list.append(command)
        self._command_index = len(self._command_list)

    def get_last_command(self):
        if len(self._command_list) == 0:
            return ''
        self._command_index -= 1
        if self._command_index < 0:
            self._command_index = 0
        return self._command_list[self._command_index]

    def get_next_command(self):
        self._command_index += 1
        if self._command_index >= len(self._command_list):
            self._command_index = len(self._command_list)
            return ''
        return self._command_list[self._command_index]

    def add_design(self, directory, offset):
        self.load_cubes_to_file(directory, False, offset)

    def subtract_design(self, directory, offset):
        try:
            file = open(directory, "r")
        except:
            print('File does not exist', flush=True)
            return
        for cube in file:
            cube_stats = cube.split(' ')
            pos = (int(cube_stats[0]) + offset[0], int(cube_stats[1]
                                                       ) + offset[1], int(cube_stats[2]) + offset[2])
            self.delete(pos)

    def get_help_description(self, option=''):
        path = os.path.dirname(os.path.realpath(__file__)) + '/command_help.json'
        with open(path) as f:
            # Load help descriptions from .json file as dict
            data = json.load(f)

        if option == '':
            return 'Possible commands:\n\n' \
                   + '\n'.join(self.get_possible_commands()) \
                   + '\n\nType help [command] to get more info on specific command.'

        # Return dict that includes command's description and example (optional)
        if option in data['commands']:
            return data['commands'][option]
        else:
            return data['commands']['no_description']

    def run_cpp(self, directory):
        print(PySlice_Tools.slice._slice.runslice(directory, self._slicerprop[0], self._slicerprop[1], self._slicerprop[2], self._slicerprop[3], self._slicerprop[4], self._slicerprop[5]))

    def add_cube_set(self, pos, dim, color=None):
        """
        Add a cube set given x, y, z position as a tuple,
        sx, sy, sz as a tuple of the cube dimension.
        Return -1 if a cube at position already exists and 1 otherwise.
        """
        (x, y, z) = pos
        (sx, sy, sz) = dim

        # If a cube is already added at the position given,
        # don't do anything
        if self.has_cube(pos):
            print('A cube has already been added at the given position', flush=True)
            return -1, 'A cube has already been added at ' + str(pos)

        if self._bound and not self.is_within_bound(pos, dim):
            return -1, 'Cube set not added because it is out of bound.'

        cubeset = CubeSet(self._ax, pos, dim, color)
        cubeset.draw()

        # resize grid if new cube is out of axis limit
        low = min(pos)
        low = min(low, self._ax.get_xlim()[0])
        high = max(x + sx, y + sy, z + sz)
        high = max(high, self._ax.get_xlim()[1])
        self._ax.set_xlim(low, high, 1)
        self._ax.set_ylim(low, high, 1)
        self._ax.set_zlim(low, high, 1)

        self._canvas.draw()

        for i in range(0, sx):
            for j in range(0, sy):
                for k in range(0, sz):
                    pos = (i + x, j + y, k + z)
                    if self.has_cube(pos):
                        self.delete_cube(pos)
                    self._cube_map[pos] = cubeset

        return 1, ''

    def delete_cube_set(self, pos, dim):
        """
        Delete a cube set given x, y, z position as a tuple,
        sx, sy, sz as a tuple of the cube dimension.
        Return -1 if cube does not exist at position and 1 otherwise.
        """
        (x, y, z) = pos
        (sx, sy, sz) = dim

        if not self.has_cube(pos):
            print('CubeSet does not exist', flush=True)
            return -1

        for i in range(0, sx):
            for j in range(0, sy):
                for k in range(0, sz):
                    pos = (i + x, j + y, k + z)
                    if self.has_cube(pos):
                        if self.is_cubeset(pos):
                            # If the cube belongs to a cube set, remove it from the cube set instead
                            self._cube_map[pos].remove_cube(pos)
                        else:
                            cube = self._cube_map[pos]
                            cube.remove()

                        del self._cube_map[pos]

        self._canvas.draw()
        return 1

    def set_bound(self, boundary):
        if self._bound:
            self._bound1.remove()
            self._bound2.remove()
            self._bound3.remove()

        self._bound = boundary
        # resize grid to boundary
        self._ax.set_xlim(boundary[0], boundary[3], 1)
        self._ax.set_ylim(boundary[1], boundary[4], 1)
        self._ax.set_zlim(boundary[2], boundary[5], 1)
        self.draw_bound(boundary)

    def draw_bound(self, boundary):
        # boundary: (min_x, min_y, min_z, max_x, max_y, max_z)
        xx, yy = np.meshgrid(
            range(boundary[0], boundary[3] + 1), range(boundary[1], boundary[4] + 1))
        zz = np.array([[boundary[2]]*(xx.shape[1])]*xx.shape[0])
        self._bound1 = self._ax.plot_surface(xx, yy, zz, color='y', alpha=0.1)

        yy, zz = np.meshgrid(
            range(boundary[1], boundary[4] + 1), range(boundary[2], boundary[5] + 1))
        xx = np.array([[boundary[0]]*yy.shape[1]]*yy.shape[0])
        self._bound2 = self._ax.plot_surface(xx, yy, zz, color='y', alpha=0.1)

        xx, zz = np.meshgrid(
            range(boundary[0], boundary[3] + 1), range(boundary[2], boundary[5] + 1))
        yy = np.array([[boundary[4]]*(xx.shape[1])]*xx.shape[0])
        self._bound3 = self._ax.plot_surface(xx, yy, zz, color='y', alpha=0.1)
        self._canvas.draw()

    def add_to_undo_stack(self, current_cube_list):
        temp = []
        for pos in current_cube_list:
            color = self._cube_map[pos]._color
            temp.append(((pos[0], pos[1], pos[2]),
                         (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))
        self._undo_stack.append(temp)

    def add_to_redo_stack(self, current_cube_list):
        temp = []
        for pos in current_cube_list:
            color = self._cube_map[pos]._color
            temp.append(((pos[0], pos[1], pos[2]),
                         (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))
        self._redo_stack.append(temp)

    def print_undo_stack(self):
        print(self._undo_stack)

    def undo(self):
        self.clear()
        for cube in self._undo_stack.pop():
            if cube[2]:
                self.add_support(cube[0])
            else:
                self.load_cube(cube[0], cube[1])
        self._canvas.draw()

    def redo(self):
        if not self._redo_stack:
            return -1
        self.clear()
        top_of_redo_stack = self._redo_stack.pop()
        for cube in top_of_redo_stack:
            if cube[2]:
                self.add_support(cube[0])
            else:
                self.load_cube(cube[0], cube[1])
        self._canvas.draw()
        return 1

    def clear_redo_stack(self):
        self._redo_stack.clear()

    def is_redo_stack_empty(self):
        if not self._redo_stack:
            return True
        else:
            return False

    def is_undo_stack_empty(self):
        if not self._undo_stack:
            return True
        else:
            return False

    def move_design(self, offset):
        temp = []
        for pos in self.get_cube_list():
            color = self._cube_map[pos]._color
            posx = pos[0] + offset[0]
            posy = pos[1] + offset[1]
            posz = pos[2] + offset[2]
            temp.append(
                ((posx, posy, posz), (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))

        self.clear()
        for cube in temp:
            if cube[2]:
                self.add_support(cube[0])
            else:
                self.load_cube(cube[0], cube[1])

        self._canvas.draw()

    def get_cube_map(self):
        return self._cube_map

    def flip_design(self):
        temp = []
        lowest = float("-inf")
        highest = float("inf")
        for pos in self.get_cube_list():
            color = self._cube_map[pos]._color
            if pos[2] > lowest:
                lowest = pos[2]
            if pos[2] < highest:
                highest = pos[2]
            temp.append(
                ((pos[0], pos[1], -pos[2]), (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))

        self.clear()
        for cube in temp:
            if cube[2]:
                self.add_support(cube[0])
            else:
                self.load_cube(cube[0], cube[1])

        self._canvas.draw()
        self.move_design((0, 0, lowest+highest))

    def rotate_design(self, degrees=90, a=0, b=0):
        # Rotation point = (a,b)
        # Positive degree rotation is in counter-clockwise
        temp = []

        if int(degrees) in [90, -270]:
            for pos in self.get_cube_list():
                color = self._cube_map[pos]._color
                temp.append(
                    ((-(pos[1] - b) + a, pos[0] - a + b, pos[2]), (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))
        elif int(degrees) in [-90, 270]:
            for pos in self.get_cube_list():
                color = self._cube_map[pos]._color
                temp.append(
                    (((pos[1] - b) + a, -(pos[0] - a) + b, pos[2]), (color[0], color[1], color[2], color[3]),self._cube_map[pos].isSupport))
        elif int(degrees) in [180, -180]:
            for pos in self.get_cube_list():
                color = self._cube_map[pos]._color
                temp.append(
                    ((-(pos[0] - b) + a, -(pos[1] - a) + b, pos[2]), (color[0], color[1], color[2], color[3]), self._cube_map[pos].isSupport))
        else:
            return

        self.clear()
        for cube in temp:
            if cube[2]:
                self.add_support(cube[0])
            else:
                self.load_cube(cube[0], cube[1])

        self._canvas.draw()

    def add_support(self, pos):
        if pos in self._cube_map:
          print('An object already exists in this location', flush=True)
          return

        support = Support(self._ax, pos, self._support_color)
        support.draw()
        self._canvas.draw()
        self._cube_map[pos] = support

    def setStartPosition(self, startPosX, startPosY):
        self._slicerprop[0] = startPosX
        self._slicerprop[1] = startPosY
        print(self._slicerprop)

    def setSpeed(self, speed):
        self._slicerprop[2] = speed
        print(self._slicerprop)

    def setExtrusion(self, extrustion):
        self._slicerprop[3] = extrustion
        print(self._slicerprop)

    def setInfill(self, infill):
        self._slicerprop[4] = infill
        print(self._slicerprop)

    def setLayerHeight(self, layerH):
        self._slicerprop[5] = layerH
        print(self._slicerprop)
