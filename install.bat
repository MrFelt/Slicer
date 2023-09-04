@echo off

REM Check if the virtual environment exists
if not exist ".\venv" (
    echo Creating virtual environment...
    call python -m venv venv || (
        echo Failed to create virtual environment.
        choice /n /c:Y /t 10 /d Y > nul
        exit /b 1
    )
)

REM Activate the virtual environment
call .\venv\Scripts\activate || (
    echo Failed to activate virtual environment.
    choice /n /c:Y /t 10 /d Y > nul
    exit /b 1
)

REM Install dependencies
call python -m pip install -r requirements.txt || (
    echo Failed to install dependencies.
    choice /n /c:Y /t 10 /d Y > nul
    exit /b 1
)

echo Dependencies installed successfully.
choice /n /c:Y /t 10 /d Y > nul
