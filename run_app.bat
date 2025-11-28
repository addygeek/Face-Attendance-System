@echo off
echo ===================================================
echo Starting Face Attendance System...
echo ===================================================
echo.
echo Starting Streamlit app...
echo If the browser doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.
".venv311\Scripts\python.exe" -m streamlit run streamlit_app.py
