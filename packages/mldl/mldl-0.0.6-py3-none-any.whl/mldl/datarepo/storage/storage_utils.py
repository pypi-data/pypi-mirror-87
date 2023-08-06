"""
Storage Utilities module
"""
from datetime import datetime, timedelta
import itertools
from typing import Iterator
from azure.storage.blob import BlobServiceClient, ContainerClient, ResourceTypes, AccountSasPermissions, generate_account_sas


def generate_azure_account_sas(connection_string: str, valid_for_hours: int = 24) -> str:
    """
    Generate SAS token for provided connection string

    Args:
        connection_string (str): connection string
        valid_for_hours (int, optional): SAS-token validity in hours. Defaults to 24.

    Returns:
        str: SAS-token
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    sas_token = generate_account_sas(
        blob_service_client.account_name,
        account_key=blob_service_client.credential.account_key,
        resource_types=ResourceTypes(object=True, container=True),
        permission=AccountSasPermissions(read=True, write=True, list=True, create=True),
        expiry=datetime.utcnow() + timedelta(hours=valid_for_hours)
    )

    return sas_token


def walk_storage_files(container_uri: str, container_path: str, page_size: int) -> Iterator[str]:
    """
    Performes storage traversal, calls new_item_lambda for every item

    Args:
        container_uri (str): Blob storage container uri
        container_path (str): Path in the container
        page_size (int): size of the page for list_blobs operation

    Yields:
        Iterator[str]: iterator over blob names, lazily following list_blobs continuation tokens
    """
    container_client = ContainerClient.from_container_url(
        container_url=container_uri)

    for blob in itertools.islice(
            container_client.list_blobs(name_starts_with=container_path, results_per_page=page_size),  # noqa: E127
            page_size):  # noqa: E127
        if blob.name.endswith("/"):
            continue
        yield blob.name
