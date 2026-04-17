#!/usr/bin/env python
"""
Django App Launcher
This script handles setup and launches the Django development server
"""
import os
import sys
import webbrowser
import time
import threading
from pathlib import Path


def get_app_dir():
    """Directory where bundled app files live (read-only when frozen)"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent


def get_data_dir():
    """Writable directory for runtime data (DB, etc.) — next to the executable"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def setup_django():
    """Setup Django environment"""
    app_dir = get_app_dir()
    data_dir = get_data_dir()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'circuit_project.settings')

    # Tell settings.py where to put the database when running as executable
    if getattr(sys, 'frozen', False):
        os.environ['DB_PATH'] = str(data_dir / 'db.sqlite3')

    sys.path.insert(0, str(app_dir))
    os.chdir(str(app_dir))

    import django
    django.setup()


def run_migrations():
    """Run database migrations"""
    print("Setting up database...")
    try:
        from django.core.management import call_command
        call_command('migrate', '--noinput', verbosity=0)
        print("Database ready")
    except Exception as e:
        print(f"Warning: Could not run migrations: {e}")


def start_server(port=8000):
    """Start the Django development server"""
    print(f"\n{'='*50}")
    print(f"Starting server on http://localhost:{port}")
    print(f"Press Ctrl+C to stop")
    print(f"{'='*50}\n")

    threading.Thread(
        target=lambda: (time.sleep(2), webbrowser.open(f'http://localhost:{port}')),
        daemon=True
    ).start()

    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', str(port), '--noreload'])


def main():
    """Main entry point"""
    print("="*50)
    print("  Excursion Estimation App")
    print("="*50)

    try:
        setup_django()
        run_migrations()
        start_server()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
