from unittest import mock
from pathlib import Path

from udemy_enroller.utils import get_app_dir


def test_get_app_dir_creates_directory_when_missing():
    """Test that get_app_dir creates the directory when it doesn't exist."""
    with mock.patch.object(Path, "home", return_value=Path("/home/testuser")):
        with mock.patch.object(Path, "mkdir") as mock_mkdir:
            result = get_app_dir()
            mock_mkdir.assert_called_once_with(exist_ok=True)
            assert result == Path("/home/testuser/.udemy_enroller")


def test_get_app_dir_returns_path():
    """Test that get_app_dir returns a Path object."""
    result = get_app_dir()
    assert isinstance(result, Path)
    assert result.name == ".udemy_enroller"
