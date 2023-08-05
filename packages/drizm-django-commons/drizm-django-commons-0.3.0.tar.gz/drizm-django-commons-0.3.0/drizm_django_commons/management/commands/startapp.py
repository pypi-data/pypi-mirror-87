from pathlib import Path

from django.conf import settings
from django.core.management.commands import startapp

from ._utils import write_file, newlines, indent


class Command(startapp.Command):
    def handle(self, *args, **options):
        APPLICATIONS_ROOT = Path(settings.BASE_DIR) / "apps"
        APP_ROOT = APPLICATIONS_ROOT / options.get("name")

        # Create the application root
        APP_ROOT.mkdir()
        (APP_ROOT / "__init__.py").touch()
        write_file(
            APP_ROOT,
            "apps.py",
            (
                "from django.apps import AppConfig",
                *newlines(2),
                "class CoreConfig(AppConfig):",
                indent(1, f"name = '{APP_ROOT.name}'"),
                indent(1, f"label = '{APP_ROOT.name}'"),
            )
        )
        write_file(
            APP_ROOT,
            "urls.py",
            (
                "from rest_framework import routers",
                *newlines(),
                "from . import views",
                "from .apps import CoreConfig as CurrentApp",
                *newlines(),
                "app_name = CurrentApp.name",
                "router = routers.SimpleRouter()",
                *newlines(),
                "urlpatterns = []",
                *newlines(),
                "urlpatterns += router.urls",
            )
        )
        write_file(
            APP_ROOT,
            "admin.py",
            (
                "from django.contrib import admin",
                *newlines(2),
                "# Register your models here"
            )
        )
        write_file(
            APP_ROOT,
            "views.py",
            (
                "from rest_framework import viewsets",
                *newlines(),
                "from .models import serializers",
                *newlines(2),
                "# Your views here"
            )
        )

        # Create the migrations directory
        migrations = APP_ROOT / "migrations"
        migrations.mkdir()
        (migrations / "__init__.py").touch()

        # Create the schemas directory
        models = APP_ROOT / "models"
        models.mkdir()
        write_file(
            models,
            "__init__.py",
            (
                "from .models import *",
            )
        )
        write_file(
            models,
            "serializers.py",
            (
                "from rest_framework import serializers",
                *newlines(2),
                "# Your serializers here",
            )
        )
        write_file(
            models,
            "models.py",
            (
                "from django.db import models",
                *newlines(2),
                "# Your models here",
                *newlines(2),
                "__all__ = []"
            )
        )

        # Create the templates directory
        templates = APP_ROOT / "templates"
        templates.mkdir()
        subfolder = templates / APP_ROOT.name
        subfolder.mkdir()
        (subfolder / ".gitkeep").touch()
