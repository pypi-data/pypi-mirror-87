""" This module provides control of application GUI.
"""

from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.figure import Figure
import wx
import wx.aui
from os import listdir, path, remove
import os

from PySlice_Tools.state import State


class TabPanel(wx.Panel):
    def __init__(self, parent, file_path=None):
        wx.Panel.__init__(self, parent)

        # Create 3d plot canvas
        fig = Figure((10, 10), 80)
        self._canvas = FigureCanvas(self, -1, fig)
        self._ax = self.set_ax(fig)

        # Create other widgets
        self._toolbar = self.make_toolbar()
        self._file_display = self.make_label()
        self._text_ctrl = self.make_textctrl()
        self._color_picker = wx.ColourPickerCtrl(self, colour=(
            0, 178, 255), style=wx.CLRP_SHOW_ALPHA, size=(80, 30))
        self._help_button = wx.Button(self, wx.ID_ANY, 'Help', (10, 10)) 
        def onHelpClick(event):
            self.display_msg('Help', self._state.get_help_description())
        self._help_button.Bind(wx.EVT_BUTTON, onHelpClick) 

        # Add color picker and its label into a sizer
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer.Add(self._text_ctrl, 1, wx.EXPAND)
        input_sizer.Add(self._color_picker, 0, wx.RIGHT)
        input_sizer.Add(self._help_button, 0, wx.RIGHT)

        # output
        self._output_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._output_Sizer.Add(self._file_display, 0, wx.EXPAND, 5)

        # Put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._canvas, 1, wx.EXPAND | wx.GROW | wx.TOP, border=-50)
        sizer.Add(self._toolbar, 0, wx.GROW)
        sizer.Add(self._output_Sizer, 0, wx.EXPAND)
        sizer.Add(input_sizer, 0, wx.EXPAND)

        # Initialize internal state
        self._state = State(self._canvas, self._ax)

        # If a file path exists, load cubes from file
        if file_path:
            res, msg = self._state.load_cubes_to_file(file_path)
            if res == -1:
                self.display_msg('Error', msg)

        self.SetSizer(sizer)
        self.Fit()

    def set_ax(self, fig):
        ax = fig.gca(projection='3d')
        ax.set_box_aspect([1, 1, 1])
        ax.set_xlim(0, 5, 1)
        ax.set_ylim(0, 5, 1)
        ax.set_zlim(0, 5, 1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        return ax

    def make_toolbar(self):
        toolbar = NavigationToolbar(self._canvas)
        # Remove the toolbar buttons that we don't need
        for i in range(5):
            toolbar.DeleteToolByPos(3)
        toolbar.Realize()

        return toolbar

    def make_textctrl(self):
        text_ctrl = wx.TextCtrl(
            self, style=wx.TE_PROCESS_ENTER, size=(100, 30))
        text_ctrl.SetFocus()
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        text_ctrl.SetFont(font)
        text_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.execute_command)

        return text_ctrl

    def make_label(self):
        label = wx.StaticText(self, style=wx.ST_ELLIPSIZE_END)
        font = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL)
        label.SetForegroundColour((0, 0, 0))
        label.SetFont(font)
        width, height = self.GetSize()
        label.Wrap(width)
        return label

    def execute_command(self, event):
        # Get command line input value
        input = self._text_ctrl.GetValue()

        # If input is empty, do nothing.
        if not input:
            return

        tokens = input.split()
        self._text_ctrl.SetValue('')
        command = tokens[0]
        size = len(tokens)
        self._state.save_command(input)

        rbg_color = self._color_picker.GetColour()
        # Matplotlib takes in normalized RBG values.
        norm_color = tuple(value / 255 for value in rbg_color)

        if command != 'undo' and command != 'redo':
            self._state.clear_redo_stack()

        if command == 'addcube':
            if size < 4:
                self.display_msg('Error', 'addcube requires x, y, z args.')
                return
            try:
                pos = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
            except ValueError:
                self.display_msg(
                    'Error', 'x, y, z are required to be of type integer.')
                return

            self._state.add_to_undo_stack(self._state.get_cube_list())
            res, msg = self._state.add_cube(pos, norm_color)

            if res == -1:
                self.display_msg('Warning', msg)
                self._state._undo_stack.pop()

            print(self._state.get_cube_list(), flush=True)
        elif command == 'del':
            if size < 4:
                self.display_msg('Error', 'delcube requires x, y, z args.')
                return

            try:
                pos = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
            except ValueError:
                self.display_msg(
                    'Error', 'x, y, z are required to be of type integer.')
                return

            self._state.add_to_undo_stack(self._state.get_cube_list())
            res = self._state.delete(pos)
            if res == -1:
                self.display_msg('Warning', 'Cube not found at ' + str(pos))
                self._state._undo_stack.pop()

            print(self._state.get_cube_list(), flush=True)
        elif command == 'save':
            if size == 1:
                self.display_msg(
                    'Error', 'save requires a filename to be specified and optionally a directory.')
                return

            if size == 3:  # If a filename and directory is passed in
                self._state.save_cubes_to_file(tokens[1], tokens[2])
                filepath = tokens[2]
                if(filepath[-1] != '/'):
                    filepath = filepath + "/"
                self.display_msg(
                    'Success', 'Model has been saved as "'+ filepath + tokens[1] + '.slice"')
            elif size == 2:  # If only a filename is passed in
                self._state.save_cubes_to_file(tokens[1])
                self.display_msg(
                    'Success', 'Model has been saved as "./'+ tokens[1] + '.slice"')
        elif command == 'clear':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            self._state.clear()
            print("Cubes cleared")
        elif command == 'load':
            if size == 1:
                self.display_msg('Error', 'load requires a file path.')
                return

            self._state.add_to_undo_stack(self._state.get_cube_list())
            if size == 2:
                res, msg = self._state.load_cubes_to_file(tokens[1])
            elif size == 3 and tokens[2] == 'f':
                res, msg = self._state.load_cubes_to_file(tokens[1], False)

            if res == -1:
                self.display_msg('Error', msg)
        elif command == 'addmodel':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            if len(tokens) == 1:
                self.display_msg(
                    'Error', 'addmodel requires a filename.'
                )
                return
            if len(tokens) == 2:
                self._state.add_design(tokens[1], (0, 0, 0))
            else:
                self._state.add_design(
                    tokens[1], (int(tokens[2]), int(tokens[3]), int(tokens[4])))
        elif command == 'submodel':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            if len(tokens) == 1:
                self.display_msg(
                    'Error', 'submodel requires a filename.'
                )
                return
            if len(tokens) == 2:
                self._state.subtract_design(tokens[1], (0, 0, 0))
            else:
                self._state.subtract_design(
                    tokens[1], (int(tokens[2]), int(tokens[3]), int(tokens[4])))
        elif command == 'help':
            if len(tokens) == 1:
                self.display_msg('Help', self._state.get_help_description())
            elif tokens[1] not in self._state.get_possible_commands():
                self.display_msg(
                    'Error', 'Invalid help argument. For a list of commands, type \'help\'.')
            else:
                help_dict = self._state.get_help_description(tokens[1])
                if 'example' in help_dict:
                    self.display_msg('Help', '\n'.join(["Command: " + tokens[1], '\n', "Description: " +
                                                        help_dict['desc'], '\n', "Example: " + help_dict['example']]))
                else:
                    self.display_msg('Help', '\n'.join(["Command: " + tokens[1], '\n', "Description: " +
                                                        help_dict['desc'], ]))
        elif command == 'slice':
            if len(tokens) == 1:
                if not self._state.get_cube_list():
                    self.display_msg(
                        'Error', 'Cannot slice an empty model.')
                    return
                self._state.save_cubes_to_file("current_design")
                self._state.run_cpp("current_design.slice")
                remove("current_design.slice")
                self.display_msg(
                    'Success', 'Model has been sliced as "./current_design.gcode"')
            else:
                if not tokens[1].endswith('.slice'):
                    self.display_msg(
                        'Error', 'File must be of type ".slice"'
                    )
                    return
                if path.exists(tokens[1]):
                    if path.getsize(tokens[1]) == 0:
                        self.display_msg(
                            'Error', 'Cannot slice an empty model.')
                        return
                    self._state.run_cpp(tokens[1])
                    self.display_msg(
                        'Success', 'Model has been sliced as "'+ tokens[1][0:-6] + '.gcode"')
                else:
                    self.display_msg(
                        'Error', 'File does not exist.'
                    )
                    return
        elif command == 'addcubeset':
            if size < 7:
                self.display_msg(
                    'Error', 'addcubeset requries x, y, z, sx, sy, sz args.')
                return
            self._state.add_to_undo_stack(self._state.get_cube_list())
            try:
                pos = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
                dim = (int(tokens[4]), int(tokens[5]), int(tokens[6]))
                res, msg = self._state.add_cube_set(pos, dim, norm_color)
                if res == -1:
                    self.display_msg('Warning', msg)
                    self._state._undo_stack.pop()
                    return
            except ValueError:
                self.display_msg(
                    'Error', 'Arguments are required to be of type integer.')
                self._state._undo_stack.pop()
                return
        elif command == 'delcubeset':
            if size != 7:
                self.display_msg(
                    'Error', 'delcubeset requries x, y, z, sx, sy, sz args.')
                return
            self._state.add_to_undo_stack(self._state.get_cube_list())
            try:
                pos = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
                dim = (int(tokens[4]), int(tokens[5]), int(tokens[6]))
                res = self._state.delete_cube_set(pos, dim)
                if res == -1:
                    self.display_msg(
                        'Warning', 'Cubeset not found at ' + str(pos))
            except ValueError:
                self.display_msg(
                    'Error', 'Arguments are required to be of type integer.')
        elif command == 'setbound':
            if size != 7:
                self.display_msg('Error', 'setbound requries min_x, min_y, min_z, max_x, max_y, max_z args.')
                return
            try:
                boundary = (int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4]), int(tokens[5]),
                            int(tokens[6]))
                self._state.set_bound(boundary)
            except ValueError:
                self.display_msg('Error', 'Arguments are required to be of type integer.')
        elif command == 'move':
            if size != 4:
                self.display_msg(
                    'Error', 'move requries x, y, z args.')
                return
            self._state.add_to_undo_stack(self._state.get_cube_list())
            try:
                offset = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
                self._state.move_design(offset)
            except ValueError:
                self.display_msg(
                    'Error', 'Arguments are required to be of type integer.')
        elif command == 'undo':
            if self._state.is_undo_stack_empty():
                self.display_msg(
                    'Error', 'No actions to undo.')
                return
            self._state.add_to_redo_stack(self._state.get_cube_list())
            self._state.undo()
        elif command == 'flip':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            self._state.flip_design()
        elif command == 'rotate':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            if size == 1:
                self._state.rotate_design()
            elif size in [2, 4]:
                try:
                    if int(tokens[1]) not in [-270, -180, -90, 90, 180, 270]:
                        self.display_msg('Error', 'Argument should be one of [-270, -180, -90, 90, 180, 270].')
                        return
                    if size == 2:
                        self._state.rotate_design(int(tokens[1]))
                    elif size == 4:
                        self._state.rotate_design(int(tokens[1]), int(tokens[2]), int(tokens[3]))
                except ValueError:
                    self.display_msg(
                        'Error', 'Arguments are required to be of type integer.')
            else:
                self.display_msg(
                        'Error', 'Incorrect arguments. Type \'help rotate\' for more info.')

        elif command == 'redo':
            if self._state.is_redo_stack_empty():
                self.display_msg(
                    'Error', 'No actions to redo.')
                return
            self._state.add_to_undo_stack(self._state.get_cube_list())
            result = self._state.redo()
        elif command == 'slicerprop':
            if tokens[1] == 'position':
                self._state.setStartPosition(int(tokens[2]), int(tokens[3]))
            elif tokens[1] == 'speed':
                self._state.setSpeed(int(tokens[2]))
            elif tokens[1] == 'extrusion':
                self._state.setExtrusion(float(tokens[2]))
            elif tokens[1] == 'infill':
                self._state.setInfill(float(tokens[2]))
            elif tokens[1] == 'layerHeight':
                self._state.setLayerHeight(float(tokens[2]))

        elif command == 'addsupport':
            self._state.add_to_undo_stack(self._state.get_cube_list())
            if size < 4:
                self.display_msg('Error', 'addsupport requires x, y, z args.')
                return
            try:
                pos = (int(tokens[1]), int(tokens[2]), int(tokens[3]))
            except ValueError:
                self.display_msg('Error', 'x, y, z are required to be of type integer.')
                return

            self._state.add_support(pos)
        else:
            self.display_msg('Error', 'Command not found.')

    def display_msg(self, title, content):
        wx.MessageBox(content, title, wx.OK | wx.ICON_INFORMATION)

    def on_key_down(self, event):
        key_pressed = event.GetKeyCode()
        self._file_display.SetLabel('')
        input = self._text_ctrl.GetValue()
        tokens = input.split()
        if key_pressed == wx.WXK_TAB:
            if len(tokens) > 0:
                if tokens[0] == 'save' or tokens[0] == 'load' or tokens[0] == 'addmodel' \
                        or tokens[0] == 'submodel' or tokens[0] == 'slice':
                    self.tab_complete_file()
                else:
                    self.tab_complete()
        elif key_pressed == wx.WXK_UP:
            self.show_last_command()
        elif key_pressed == wx.WXK_DOWN:
            self.show_next_command()
        else:
            event.Skip()
            return

    def tab_complete(self):
        current_text = self._text_ctrl.GetValue()
        options = [cmd for cmd in self._state.get_possible_commands() if
                   cmd.startswith(current_text)]  # Grab possible commands based on current text input
        common_prefix = self.longestCommonPrefix(options)
        if common_prefix != '':
            # Set text to only possible command
            self._text_ctrl.ChangeValue(common_prefix)
            self._text_ctrl.SetInsertionPointEnd()  # Set cursor to EOL

    def tab_complete_file(self):
        filedir = self._text_ctrl.GetValue()
        tokens = filedir.split()
        if len(tokens) == 2 and tokens[0] != 'save':
            text = tokens[1]
        elif len(tokens) == 3 and tokens[0] == 'save':
            text = tokens[2]
        elif len(tokens) > 2:
            return
        else:
            text = ''

        path_list = text.split('/')
        current_text = path_list.pop(len(path_list) - 1)
        # print('Current Text: ' + current_text)
        # print(path_list)
        filepath = ""
        for p in path_list:
            filepath += p + '/'

        if filepath == "":
            test = listdir()
        else:
            try:
                test = listdir(filepath)
                self._file_display.SetLabel(str(test))
                print(test)
            except:
                print("No file path")
                return

        options = [file for file in test if
                   file.startswith(current_text)]  # Grab possible commands based on current text input
        common_prefix = self.longestCommonPrefix(options)
        if common_prefix != '':
            if path.isdir(filepath + common_prefix):
                common_prefix += "/"
            if len(tokens) == 3 and tokens[0] == 'save':
                self._text_ctrl.ChangeValue(
                    tokens[0] + ' ' + tokens[1] + ' ' + filepath + common_prefix)
            else:
                self._text_ctrl.ChangeValue(
                    tokens[0] + ' ' + filepath + common_prefix)  # Set text to only possible command
            self._text_ctrl.SetInsertionPointEnd()  # Set cursor to EOL

    def show_last_command(self):
        last_command = self._state.get_last_command()
        if last_command:
            self._text_ctrl.SetValue(last_command)
            self._text_ctrl.SetInsertionPointEnd()

    def show_next_command(self):
        next_command = self._state.get_next_command()
        self._text_ctrl.SetValue(next_command)
        self._text_ctrl.SetInsertionPointEnd()

    def longestCommonPrefix(self, str_list):
        # From https://www.studytonight.com/post/finding-longest-common-prefix-in-a-list-of-strings-in-python
        if not str_list:
            return ''
        if len(str_list) == 1:
            return str_list[0]
        str_list.sort()
        shortest = str_list[0]
        prefix = ''
        for i in range(len(shortest)):
            if str_list[len(str_list) - 1][i] == shortest[i]:
                prefix += str_list[len(str_list) - 1][i]
            else:
                break
        return prefix


class AppFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='PySlice', pos=(0, 0), size=(800, 850))
        self._project_id = 1
        self._tab_count = 0

        # Create a panel and notebook (tabs holder)
        # https://pythonspot.com/wxpython-tabs/
        self._panel = wx.Panel(self)
        self._notebook = wx.aui.AuiNotebook(self._panel)

        # Create a project tab
        tab = TabPanel(self._notebook)
        self._notebook.AddPage(tab, 'Project %d' % self._project_id)
        self._tab_count += 1

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._notebook, 1, wx.EXPAND)
        self._panel.SetSizer(sizer)
        self.set_menubar()
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.close_tab, self._notebook)

    def set_menubar(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()

        # Create new file button
        new = wx.MenuItem(file_menu, wx.ID_NEW,
                          text='New File', kind=wx.ITEM_NORMAL)
        file_menu.Append(new)

        # Create open file button
        open_file = wx.MenuItem(file_menu, wx.ID_OPEN,
                                text='Open File', kind=wx.ITEM_NORMAL)
        file_menu.Append(open_file)

        # Create save as button
        save_as = wx.MenuItem(file_menu, wx.ID_SAVEAS,
                                text='Save As...', kind=wx.ITEM_NORMAL)
        file_menu.Append(save_as)

        # Close current project button
        close = wx.MenuItem(file_menu, wx.ID_CLOSE,
                            text='Close Current', kind=wx.ITEM_NORMAL)
        file_menu.Append(close)

        # Quit application
        quit = wx.MenuItem(file_menu, wx.ID_EXIT,
                           text='Quit', kind=wx.ITEM_NORMAL)
        file_menu.Append(quit)

        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.menu_handler)

    def menu_handler(self, event):
        id = event.GetId()
        if id == wx.ID_NEW:
            self.add_tab()
        elif id == wx.ID_OPEN:
            open_file_dialog = wx.FileDialog(self, "Open", "", "",
                                             "Slice files (*.slice)|*.slice",
                                             wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if open_file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            file_path = open_file_dialog.GetPath()
            self.add_tab(file_path)
        elif id == wx.ID_SAVEAS:
            save_as_dialog = wx.FileDialog(self, "Save As", "", "", 
                                            "Slice files (*.slice)|*.slice",
                                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if save_as_dialog.ShowModal() == wx.ID_CANCEL:
                return
            file_path = save_as_dialog.GetPath()
            save_dir = file_path.rsplit('/',1)[0]
            save_filename = file_path.rsplit('/',1)[1]

            # If replacing previously saved file, remove .slice from end of filename to pass into save function
            if save_filename.endswith('.slice'):    
                save_filename = save_filename.rsplit('.',1)[0]
            self._notebook.GetCurrentPage()._state.save_cubes_to_file(save_filename, save_dir)

        elif id == wx.ID_CLOSE:
            self.remove_tab()
        elif id == wx.ID_EXIT:
            self.Close()

    def add_tab(self, file_path=None):
        self._project_id += 1
        self._tab_count += 1
        new_tab = TabPanel(self._notebook, file_path)
        self._notebook.AddPage(new_tab, 'Project %d' % self._project_id)
        self._notebook.SetSelection(self._tab_count - 1)

    def remove_tab(self):
        if self._tab_count > 0:
            self._tab_count -= 1
            self._notebook.RemovePage(self._notebook.GetSelection())

    def close_tab(self, event):
        self._tab_count -= 1
