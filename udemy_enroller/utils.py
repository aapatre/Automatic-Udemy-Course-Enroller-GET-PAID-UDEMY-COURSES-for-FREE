"""Utility functions."""

from pathlib import Path


def get_app_dir() -> Path:
    """
    Get the app directory where all data related to the script is stored.

    :return: Path to the app directory
    """
    app_dir = Path.home() / ".udemy_enroller"
    app_dir.mkdir(exist_ok=True)
    return app_dir
