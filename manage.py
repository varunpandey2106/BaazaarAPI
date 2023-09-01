#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BaazaarAPI.settings.base')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "allauth needs to be added to INSTALLED_APPS.") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
