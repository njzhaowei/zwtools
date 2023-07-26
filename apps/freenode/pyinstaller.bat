@echo off
set EXE_NAME=freenode
title %EXE_NAME%-%date%-%time%-%cd%
.\.venv\Scripts\python.exe ../../scripts/pyinstaller.py -o %EXE_NAME% -specfile pyinstaller_win.spec -upxdir ../../bin --onefile --console
pause