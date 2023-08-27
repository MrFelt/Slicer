@echo off

REM Check if the virtual environment exists
if not exist ".\venv" (
    echo Creating virtual environment...
    call python -m venv venv
    call .\venv\Scripts\activate
    call python -m pip install -r requirements.txt
    pause
) else (
    call .\venv\Scripts\activate
    call python -m pip install -r requirements.txt
    echo Installed dependencies / Updated dependencies, please run start.bat or whisper.bat...
    pause
)
