# pylint: disable-all
# flake8: noqa
"""
Unit tests for main CLI module
"""
from unittest.mock import Mock, patch, MagicMock, mock_open
import glob
import builtins
from functools import partial
from pathlib import Path
from ...datarepo.storage.azure_blob import AzureBlobStorage
from azure.storage.blob import ContainerClient
from ..cli_main import main


_TEST_CONTAINER_URL = "https://fake.blob.core.windows.net/containername"
_TEST_PATH_NAME = "folder/subfolder"

_original_open = builtins.open


class FakeBlob:
    def __init__(self, name):
        self.name = name


def _mock_list_blobs(*args, **kwargs):
    blobs = [
        FakeBlob('folder/subfolder/file1.mp4'),
        FakeBlob('folder/subfolder/subfolder2/'),
        FakeBlob('folder/subfolder/subfolder2/file2.mp4')
    ]

    return iter(blobs)


def _write_func(text):
    assert text == "filename\n" or text == "file1.mp4\n" or text == "subfolder2/file2.mp4\n"

def _get_fake_config():
    fake_text = f"data_azure_storage_container_uri: \"{_TEST_CONTAINER_URL}\"\n"
    fake_text += f"data_azure_storage_path: \"{_TEST_PATH_NAME}\"\n"
    fake_text += "data_azure_storage_connection_string: \"DefaultEndpointsProtocol=https;" \
                "AccountName=fake;AccountKey=123==;EndpointSuffix=core.windows.net\""
    return fake_text

def _mocked_file(m, fn, *args, **kwargs):
    m.opened_file = Path(fn)
    if fn.endswith(".csv"):
        file_obj = mock_open(read_data="").return_value
        file_obj.write = _write_func
        return file_obj
    elif fn.endswith("datarepo.yml"):
        confix_text = _get_fake_config()
        return mock_open(read_data=confix_text).return_value
    else:
        return _original_open(fn, *args, **kwargs)

def _create_mock_open():
    mock = mock_open(read_data='')
    mock.side_effect = partial(_mocked_file, mock)
    return mock

def _always_exists(_):
    return True

def test_cli_parameters_success():
    try:
        my_open = _create_mock_open()

        with patch('azure.storage.blob.ContainerClient.list_blobs', _mock_list_blobs):
            with patch('builtins.open', my_open, create=True):
                with patch('os.path.exists', _always_exists, create=True):
                    main(["-s", "list", "-l", "dataset/labels/listed", "--group_len", "10"])
        
        assert True
    except:
        assert False


def test_cli_parameters_fail():
    try:
        main(["-s", "list", "-l", "dataset/labels/listed", "--group_len", "10"])
        assert False
    except SystemExit as ex:
        assert ex.code == 255
