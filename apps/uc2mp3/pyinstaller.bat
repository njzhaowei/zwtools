@echo off
.\.venv\Scripts\python.exe ../../scripts/pyinstaller.py -o uc2mp3 -specfile pyinstaller_win.spec -upxdir ../../bin --onefile --console
pause