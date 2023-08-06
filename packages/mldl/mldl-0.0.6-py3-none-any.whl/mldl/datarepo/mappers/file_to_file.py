# pylint: disable=unnecessary-pass,too-few-public-methods
"""
File-to-file static mapper:
maps a label/annotation file to a data file in a remote storage
with the same name and relative location
"""
import os
import glob
from typing import List
from .static_file_mapper import StaticFileMapper


class FileToFileMapper(StaticFileMapper):
    """
    File to File Mapper

    Attributes
    ----------
    labels_pattern : str
        pattern for using with glob.iglob when getting CSV files
    data_extension : str
        data files extension

    Methods
    -------
    map_files():
        Performs file mapping.
    """

    def __init__(self, cache_dir: str, labels_dir: str, labels_pattern: str, data_extension: str):
        """
        Initializes file mapper

        Args:
            cache_dir (str): data cache directory
            labels_dir (str): labels directory
            labels_pattern (str): labels pattern
            data_extension (str): data files extension
        """
        super().__init__(cache_dir, labels_dir)
        self.labels_pattern = labels_pattern
        self.data_extension = data_extension

        if not self.data_extension.startswith("."):
            self.data_extension = f".{self.data_extension}"

    def map_files(self) -> List[str]:
        """
        Performes file mapping. Derived classes must override it.

        Returns:
            List[str]: list of mapped files
        """
        paths = []

        for file in glob.iglob(os.path.join(self.labels_dir, self.labels_pattern), recursive=True):
            pre, _ = os.path.splitext(file)
            file = pre + self.data_extension

            rel_path = os.path.relpath(file, self.labels_dir)
            paths.append(rel_path)
        return paths
