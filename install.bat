@echo off

REM Check if the virtual environment exists
if not exist ".\venv" (
    echo Creating virtual environment...
    call python -m venv venv
    call .\venv\Scripts\activate
    call python -m pip install -r requirements.txt
    pause
) else (
    echo Virtual environment already exists, running start.bat...
    call start.bat
)
