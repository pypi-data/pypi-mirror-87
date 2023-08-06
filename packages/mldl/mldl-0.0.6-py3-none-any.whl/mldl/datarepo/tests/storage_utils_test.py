# pylint: disable-all
# flake8: noqa
"""
Unit tests for Azure Blob Storage utils (storage_utils.py)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ..storage.storage_utils import walk_storage_files, generate_azure_account_sas
from azure.storage.blob import ContainerClient

_TEST_CONN_STR = "DefaultEndpointsProtocol=https;AccountName=fake;AccountKey=23423423423423423423==;"\
                "EndpointSuffix=core.windows.net"
_TEST_CONTAINER_URL = "https://fake.blob.core.windows.net/containername"
_TEST_PATH_NAME = "folder/subfolder"

def test_sas_success():
    sas_token = generate_azure_account_sas(
        _TEST_CONN_STR,
        1)
    assert sas_token is not None and sas_token != ""


def test_sas_fail():
    try:
        sas_token = generate_azure_account_sas(
            "AccountKey=23423423423423423423==",
            1)
        assert False
    except ValueError:
        assert True
    except:
        assert False

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


def test_walk_storage_files_success():
    with patch('azure.storage.blob.ContainerClient.list_blobs', _mock_list_blobs):
        files_iter = walk_storage_files(
            container_uri=_TEST_CONTAINER_URL,
            container_path=_TEST_PATH_NAME,
            page_size=100)
        files = list(files_iter)
        assert len(files) == 2
        assert files[0] == 'folder/subfolder/file1.mp4'
        assert files[1] == 'folder/subfolder/subfolder2/file2.mp4'
