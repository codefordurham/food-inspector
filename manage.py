#!/usr/bin/env python
import os
import sys

from eatsmart import load_env

load_env.load_env()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eatsmart.settings")
    print(os.environ['DJANGO_SETTINGS_MODULE'])

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
