import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def azure_blob_get(account_name, account_key,
                   container_name, blob_name):
    """Return json format."""
    conn_str = f'DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    # container_client = blob_service_client.create_container(container_name)
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name)
    return json.loads(blob_client.download_blob().readall())


def azure_blob_upload(account_name, account_key,
                      container_name, blob_name, file_path):
    """Upload file (path) to blob."""
    conn_str = f'DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    # container_client = blob_service_client.create_container(container_name)
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name)
    if blob_client.exists():
        blob_client.delete_blob()
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    print('### bon azure blob ###')
