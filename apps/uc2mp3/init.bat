python -m venv .\.venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -U -r .\requirements.txt
.\.venv\Scripts\pip install -U -r .\requirements_dev.txt
@echo off
pause