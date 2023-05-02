@echo off
.\.venv\Scripts\python.exe ../../scripts/pyinstaller.py -o pdftitle -specfile pyinstaller_win.spec -upxdir ../../bin --onefile --console
pause