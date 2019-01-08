#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
<<<<<<< HEAD
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.settings.dev')
=======
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.config.settings')
>>>>>>> 4d5ac44122f34c6ece503f4efe13f1e41b918d0c
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
