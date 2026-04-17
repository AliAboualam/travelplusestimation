@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: install.bat — Sets up the Excursion Estimation project
:: Requires Python 3.12+ to be installed and on PATH
:: Run from the excursionEstimation\ folder
:: ============================================================

echo.
echo ============================================================
echo  Excursion Estimation — Dependency Installer
echo ============================================================
echo.

:: ── 1. Check Python ─────────────────────────────────────────

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.12+ from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Found Python %PYVER%

:: ── 2. Create virtual environment ───────────────────────────

if not exist ".venv\" (
    echo.
    echo [INFO] Creating virtual environment in .venv\ ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists, skipping creation.
)

:: ── 3. Activate virtual environment ─────────────────────────

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.

:: ── 4. Upgrade pip ──────────────────────────────────────────

echo.
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip up to date.

:: ── 5. Install dependencies ──────────────────────────────────

echo.
echo [INFO] Installing packages from requirements.txt...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Package installation failed. Check requirements.txt and your internet connection.
    pause
    exit /b 1
)
echo [OK] All packages installed.

:: ── 6. Run Django migrations ─────────────────────────────────

echo.
echo [INFO] Applying Django database migrations...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo [ERROR] Migration failed.
    pause
    exit /b 1
)
echo [OK] Database ready.

:: ── 7. Done ──────────────────────────────────────────────────

echo.
echo ============================================================
echo  Setup complete!
echo.
echo  To start the development server:
echo    Double-click run.bat  (or run it from this folder)
echo.
echo  Then open http://127.0.0.1:8000/ in your browser.
echo ============================================================
echo.
pause
