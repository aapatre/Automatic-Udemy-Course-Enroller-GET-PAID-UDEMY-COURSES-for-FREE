import runpy
from unittest import mock


def test_run_enroller_entry_point():
    """Test that run_enroller.py calls main() when executed as __main__."""
    with mock.patch("udemy_enroller.cli.main") as mock_main:
        runpy.run_module("run_enroller", run_name="__main__")
        mock_main.assert_called_once()
