# pylint: disable-all
# flake8: noqa
"""
Unit tests for mappers
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import glob
import builtins
from ..mappers.csv_to_file import CSVToFileMapper
from ..mappers.file_to_file import FileToFileMapper


def _fake_iglob(pathname, *, recursive=False):
    return ['1.csv']


def _fake_rel_path(path, start=None):
    return path


def test_csv_mapper():
    my_open = mock_open(read_data='filename\n00000000.jpg\n')
    with patch('builtins.open', my_open, create=True):
        with patch('glob.iglob', _fake_iglob, create=True):
            mapper = CSVToFileMapper("cache", "labels", ".csv")
            files = mapper.map_files()
            assert len(files) == 1
            assert files[0] == "00000000.jpg"


def test_file_mapper():
    with patch('glob.iglob', _fake_iglob, create=True):
        with patch('os.path.relpath', _fake_rel_path, create=True):
            mapper = FileToFileMapper("cache", "labels", ".csv", ".mp4")
            files = mapper.map_files()
            assert len(files) == 1
            assert files[0] == "1.mp4"
