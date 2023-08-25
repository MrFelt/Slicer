@echo off

echo Activating virtual environment...
call .\venv\Scripts\activate

echo Running init.py...
call python init.py

pause
