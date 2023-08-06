# pylint: disable=unnecessary-pass,too-few-public-methods
"""
Base class for remote storage providers
"""
from typing import List


class Storage:
    """
    Base class for storage providers.
    """
    def __init__(self, cache_dir: str, storage_container_uri: str, storage_path: str = None):
        """
        Initializes storage provider

        Args:
            cache_dir (str): data cache directory
            storage_container_uri (str): remote storage container uri
            storage_path (str, optional): remote storage path under container. Defaults to None.
        """
        self.cache_dir = cache_dir
        self.storage_container_uri = storage_container_uri
        self.storage_container_name = storage_container_uri.rsplit('/', 1)[-1]
        self.storage_path = storage_path

    def authenticate(self, sas_token: str):
        """
        Uses provided security token for authentication on the remote storage

        Args:
            sas_token (str): security token
        """
        pass

    def is_cached(self, path: str) -> bool:
        """
        Checks if provided item is in the data cache

        Args:
            path (str): item to check

        Returns:
            bool: True if provided item is in the data cache
        """
        pass

    def get_cached_path(self, path: str) -> str:
        """
        returns full path to a locally cached item

        Args:
            path (str): item to return local path for

        Returns:
            str: full local path
        """
        pass

    def cache_items(self, paths: List[str]) -> bool:
        """
        Performes caching operation for provided items

        Args:
            paths (List[str]): List of items to cache

        Returns:
            bool: True if operation was successful
        """
        pass

    def generate_storage_lists(self, group_len: int):
        """
        Generates lists with all items in the remote storage
        and saves them to files with group_len items per file.
        Files are saved to cache_dir.

        Args:
            group_len (int): maximum number of items per file
        """
        pass
