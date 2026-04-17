"""
Entry point — runs the Django development server.
Execute from the excursionEstimation/ directory:

    python templates/backend.py runserver
    # or simply:
    python manage.py runserver
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "circuit_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is not installed in the current environment.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Default to runserver if no argument given
    if len(sys.argv) == 1:
        sys.argv.append("runserver")
    main()
