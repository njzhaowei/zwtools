import sys
import wx
from pathlib import Path

EXE_PTH = Path(sys.argv[0]).resolve()
CWD_DIR = Path(sys.argv[0]).parent.resolve()
TMP_DIR = Path(__file__).parent.parent.resolve()

#pylint: disable=no-member
if __name__ == '__main__':
    print('EXE_PATH: %s, CWD_DIR: %s, TMP_DIR: %s'%(EXE_PTH, CWD_DIR, TMP_DIR))
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
    frame.Show(True)     # Show the frame.
    app.MainLoop()
