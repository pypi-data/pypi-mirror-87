# pylint: disable-all
# flake8: noqa
"""
Unit tests for Azure Blob Storage (azure_blob.py)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from typing import Callable
from functools import partial
from pathlib import Path
import builtins
from ..storage.azure_blob import AzureBlobStorage
from azure.storage.blob import ContainerClient

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

def _mocked_file(m, fn, *args, **kwargs):
    m.opened_file = Path(fn)
    if not fn.endswith(".csv"):
        return _original_open(fn, *args, **kwargs)
    file_obj = mock_open(read_data="").return_value
    file_obj.write = _write_func
    return file_obj


def _create_mock_open():
    mock = mock_open(read_data='')
    mock.side_effect = partial(_mocked_file, mock)
    return mock


def test_generate_storage_lists():
    blob_storage = AzureBlobStorage(
        "cache", _TEST_CONTAINER_URL, _TEST_PATH_NAME)
    
    my_open = _create_mock_open()

    with patch('azure.storage.blob.ContainerClient.list_blobs', _mock_list_blobs):
        with patch('builtins.open', my_open, create=True):
            blob_storage.generate_storage_lists(10)
