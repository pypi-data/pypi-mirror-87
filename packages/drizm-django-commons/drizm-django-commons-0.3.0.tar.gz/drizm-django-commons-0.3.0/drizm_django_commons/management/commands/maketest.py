from pathlib import Path

from django.core.management.base import AppCommand
from django.conf import settings
from ._utils import write_file, newlines, indent


class Command(AppCommand):
    def handle_app_config(self, app_config, **options):
        TESTS_ROOT = Path(settings.BASE_DIR).parent / "tests" / "integration"
        write_file(
            TESTS_ROOT,
            f"test_{app_config.label}",
            (
                "from rest_framework import status",
                "from rest_framework.reverse import reverse",
                "from rest_framework.test import APITestCase",
                *newlines(2),
                f"class Test{app_config.label.capitalize()}(APITestCase):",
                indent(1, "pass")
            )
        )
