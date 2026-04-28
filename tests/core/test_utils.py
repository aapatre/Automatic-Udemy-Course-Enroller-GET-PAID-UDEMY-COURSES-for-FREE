from unittest import mock

from udemy_enroller.utils import get_app_dir


def test_get_app_dir_creates_directory_when_missing():
    """Test that get_app_dir creates the directory when it doesn't exist (line 16)."""
    with mock.patch("os.path.isdir", return_value=False):
        with mock.patch("os.mkdir") as mock_mkdir:
            with mock.patch("os.path.expanduser", return_value="/home/testuser"):
                result = get_app_dir()
                mock_mkdir.assert_called_once_with("/home/testuser/.udemy_enroller")
                assert result == "/home/testuser/.udemy_enroller"
