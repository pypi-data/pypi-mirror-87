# pylint: disable=bad-option-value,missing-return-doc
"""
A storage provider for working with files Azure Blob Storage
"""
import os
import uuid
from typing import List
import subprocess
from .storage import Storage
from .storage_utils import walk_storage_files


class AzureBlobStorage(Storage):
    """
    Storage provider implementation class for working with files Azure Blob Storage
    """
    _MAX_LIST_GROUP_LEN = 5000
    _PROCESS_TIMEOUT = 96 * 3600

    def __init__(self, cache_dir: str, storage_container_uri: str, storage_path: str = None):
        """
        Initializes storage provider

        Args:
            cache_dir (str): data cache directory
            storage_container_uri (str): remote storage container uri
            storage_path (str, optional): remote storage path under container. Defaults to None.
        """
        self.sas_token = ""
        super().__init__(cache_dir, storage_container_uri, storage_path)

    def authenticate(self, sas_token: str):
        """
        Uses provided security token for authentication on the remote storage

        Args:
            sas_token (str): SAS-token to use with storage operations
        """
        if sas_token is not None:
            if sas_token.startswith("?"):
                self.sas_token = sas_token
            else:
                self.sas_token = f"?{sas_token}"
        else:
            self.sas_token = ""

    def is_cached(self, path: str) -> bool:
        """
        Checks if provided item is in the data cache

        Args:
            path (str): item to check

        Returns:
            bool: True if provided item is in the data cache
        """
        return os.path.exists(self.get_cached_path(path))

    def get_cached_path(self, path: str) -> str:
        """
        returns full path to a locally cached item

        Args:
            path (str): item to return local path for

        Returns:
            str: full local path
        """
        if self.storage_path is not None:
            return os.path.join(self.cache_dir, self.storage_container_name, self.storage_path, path)
        else:
            return os.path.join(self.cache_dir, self.storage_container_name, path)

    def cache_items(self, paths: List[str]) -> bool:
        """
        Performes caching operation for provided items

        Args:
            paths (List[str]): List of items to cache

        Returns:
            bool: True if operation was successful
        """
        return self._az_copy(paths) == 0

    def generate_storage_lists(self, group_len: int):
        """
        Generates lists with all items in the remote storage
        and saves them to files with group_len items per file.
        Files are saved to cache_dir.

        Args:
            group_len (int): maximum number of items per file
        """
        container_uri = self.storage_container_uri
        if self.sas_token is not None and self.sas_token != "":
            container_uri += self.sas_token

        stg_path = self.storage_path
        if stg_path is not None and not stg_path.endswith("/"):
            stg_path += "/"

        current_group = []
        group_number = 0

        for blob in walk_storage_files(container_uri, stg_path, AzureBlobStorage._MAX_LIST_GROUP_LEN):
            if stg_path is not None:
                blob = blob[len(stg_path):]
            current_group.append(blob)
            if len(current_group) == group_len:
                self._store_list(group_number, current_group)
                current_group = []
                group_number += 1

        if len(current_group) != 0:
            self._store_list(group_number, current_group)

    def _store_list(self, list_number: int, file_list: List[str]):
        # 8-digit file names, padded with zeros if needed (00000001.csv)
        file_path = f"{self.cache_dir}/{list_number:08}.csv"

        with open(file_path, 'w') as file_obj:
            file_obj.write("filename\n")
            for item in file_list:
                file_obj.write(f"{item}\n")

    def _get_item_uri(self, local_path: str) -> str:
        if self.storage_path is not None:
            uri = f"{self.storage_container_uri}/{self.storage_path}/{local_path}"
        else:
            uri = f"{self.storage_container_uri}/{local_path}"
        if self.sas_token is not None and self.sas_token != "":
            uri += self.sas_token
        return uri

    def _az_copy(self, paths: List[str], cwd=None) -> int:
        tmp_list_name = f"{uuid.uuid1()}.list.txt"
        tmp_list_path = self.get_cached_path(tmp_list_name)  # temporary file in the cache
        dir_name = os.path.dirname(tmp_list_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            with open(tmp_list_path, "w") as tmp_list_file:
                for path in paths:
                    if self.storage_path is not None:
                        tmp_list_file.write(f"{self.storage_path}/{path}\n")
                    else:
                        tmp_list_file.write(f"{path}\n")

        container_uri = self.storage_container_uri
        if self.sas_token is not None and self.sas_token != "":
            container_uri += self.sas_token
        destination = self.cache_dir

        command = f"azcopy cp \"{container_uri}\" \"{destination}\" --list-of-files \"{tmp_list_path}\" "\
                    "--overwrite ifSourceNewer --log-level ERROR"  # noqa: E127
        process = subprocess.Popen(command, cwd=cwd, shell=True)
        try:
            process.wait()
            code = process.poll()
        except subprocess.TimeoutExpired:
            process.kill()
            code = 1

        os.remove(tmp_list_path)

        return code
