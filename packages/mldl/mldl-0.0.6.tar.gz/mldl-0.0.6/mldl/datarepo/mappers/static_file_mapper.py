# pylint: disable=unnecessary-pass,too-few-public-methods
"""
Base class for static file mappers
"""
from typing import List


class StaticFileMapper:
    """
    File to File Mapper

    Attributes
    ----------
    cache_dir : str
        Data cache directory
    labels_dir : str
        Labels directory

    Methods
    -------
    map_files():
        Performes file mapping. Derived classes must override it.
    """
    def __init__(self, cache_dir: str, labels_dir: str):
        """
        Initializes file mapper

        Args:
            cache_dir (str): [description]
            labels_dir (str): [description]
        """
        self.cache_dir = cache_dir
        self.labels_dir = labels_dir

    def map_files(self) -> List[str]:
        """
        Performes file mapping. Derived classes must override it.

        Returns:
            List[str]: list of mapped files
        """
        pass
