@echo off

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run pytest
pytest

@echo on
