@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: run.bat — Starts the Excursion Estimation development server
:: Run install.bat first if you haven't already.
:: Run from the excursionEstimation\ folder
:: ============================================================

echo.
echo ============================================================
echo  Excursion Estimation — Development Server
echo ============================================================
echo.

:: ── 1. Check virtual environment exists ─────────────────────

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo         Please run install.bat first.
    pause
    exit /b 1
)

:: ── 2. Activate virtual environment ─────────────────────────

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.

:: ── 3. Start Django development server ──────────────────────

echo.
echo [INFO] Starting server at http://127.0.0.1:8000/
echo        Press Ctrl+C to stop.
echo.
python manage.py runserver
