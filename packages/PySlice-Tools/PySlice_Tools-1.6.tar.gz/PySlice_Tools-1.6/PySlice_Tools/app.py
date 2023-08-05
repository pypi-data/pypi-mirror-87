import wx

from PySlice_Tools.gui import AppFrame

class PySlice(wx.App):
    def OnInit(self):
        frame = AppFrame()
        frame.Show(True)
        return True


def main():
    app = PySlice()
    app.MainLoop()
    
if __name__ == '__main__':
    main()
