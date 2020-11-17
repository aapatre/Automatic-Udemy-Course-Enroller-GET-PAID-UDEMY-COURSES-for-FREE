import os
import pytest
import shutil


@pytest.fixture(scope="session", autouse=True)
def test_file_dir():
    test_file_dir = "test_tmp"
    # Try to delete directory in case it wasn't deleted after last test run
    if os.path.isdir(test_file_dir):
        shutil.rmtree(test_file_dir)
    yield os.mkdir(test_file_dir)
    # Delete directory after all tests completed
    if os.path.isdir(test_file_dir):
        shutil.rmtree(test_file_dir)
