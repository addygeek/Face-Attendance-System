@echo off
echo ===================================================
echo Face Attendance System Launcher
echo ===================================================
echo.
echo Checking for Python 3.11 environment...

if exist ".venv311\Scripts\python.exe" (
    echo Found .venv311 environment.
    echo Starting application...
    ".venv311\Scripts\python.exe" -m streamlit run streamlit_app.py
) else (
    echo ERROR: .venv311 environment not found!
    echo Please run setup_env.bat first or ensure you have Python 3.11 installed.
    echo.
    echo Current Python version (may be incompatible):
    python --version
)

pause
