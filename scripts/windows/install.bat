@echo off

REM Check if a virtual environment is currently activated
if defined VIRTUAL_ENV (
    echo Virtual environment detected at: %VIRTUAL_ENV%
    echo Please deactivate the virtual environment before proceeding.
    echo Use the command: deactivate
    pause
    exit /b
) else (
    echo No virtual environment currently activated. Proceeding...
)

REM Check if .venv directory exists
if exist .venv (
    echo Removing existing virtual environment directory...
    rmdir /s /q .venv
) else (
    echo No existing virtual environment directory found. Proceeding to create a new one...
)

REM Create a new virtual environment
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Install the required packages
pip install -r requirements.txt

@echo on
