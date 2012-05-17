#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rateout.settings")

    from django.core.management import execute_from_command_line
    from validation.views import validate_production_data
    validate_production_data()

