@echo off
set tmpdir=..\tmp

for %%A in (%cd%\..) do (
  set ppd=%%~nxA
)
echo ppd: %ppd%

..\.venv\Scripts\nuitka.bat ^
    --follow-imports ^
    --standalone ^
    --onefile ^
    --windows-onefile-tempdir-spec=%TEMP%\%ppd% ^
    --windows-disable-console ^
    --output-dir=%tmpdir% ^
    --windows-icon-from-ico=..\imgs\logo.ico ^
    -o %tmpdir%\%ppd%.exe ^
    ..\main.py
pause