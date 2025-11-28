@echo off
echo ===================================================
echo Face Attendance System Setup
echo ===================================================
echo.

echo This script will help you set up the environment.
echo NOTE: You must have Python 3.11 installed on your system.
echo.

python --version
echo.

if exist ".venv311" (
    echo Virtual environment .venv311 already exists.
    echo Installing dependencies...
    ".venv311\Scripts\python.exe" -m pip install -r requirements.txt
) else (
    echo Creating virtual environment .venv311...
    echo Attempting to find Python 3.11...
    
    py -3.11 -m venv .venv311
    if errorlevel 1 (
        echo.
        echo Could not create venv with 'py -3.11'. Trying 'python3.11'...
        python3.11 -m venv .venv311
    )
    
    if exist ".venv311" (
        echo.
        echo Environment created successfully!
        echo Installing dependencies...
        ".venv311\Scripts\python.exe" -m pip install -r requirements.txt
    ) else (
        echo.
        echo CRITICAL ERROR: Could not create Python 3.11 environment.
        echo Please install Python 3.11 from python.org and try again.
        echo Your current default python is:
        python --version
        echo This version is likely incompatible with MediaPipe.
        pause
        exit /b
    )
)

echo.
echo Setup complete!
echo You can now run the app using run_app.bat
echo.
pause
