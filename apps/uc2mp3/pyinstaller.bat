@echo off
set EXE_NAME=uc2mp3
title %EXE_NAME%-%date%-%time%-%cd%
.\.venv\Scripts\python.exe ../../scripts/pyinstaller.py -o %EXE_NAME% -specfile pyinstaller_win.spec -upxdir ../../bin --onefile --console
pause