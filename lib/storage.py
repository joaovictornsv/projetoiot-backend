import re
import os
import base64
from azure.storage.blob import (BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings)
from datetime import (datetime, timedelta)
CONNECTION_STRING = os.environ['AZURE_STORAGE_IMAGES_CONNECTION_STRING']
AZURE_PRIMARY_KEY = os.environ['AZURE_STORAGE_IMAGES_PRIMARY_KEY']


def generate_sas_url(file_name, container):
    sas = generate_blob_sas(
        account_name="saprojetoiotimages",
        account_key=AZURE_PRIMARY_KEY,
        container_name=container,
        blob_name=file_name,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=2)
    )

    sas_url = 'https://saprojetoiotimages.blob.core.windows.net/'+container+'/'+file_name+'?'+sas
    return sas_url


def upload_blob(data, filename, container):
    # Base64 string representation of data (ex: profile image sent through JSON REST request)
    content_type, buffer = re.match("^data:([A-Za-z-+\/]+);base64,(.+)$", data).groups()
    _, extension = content_type.split('/')
    filename_with_extension = f'{filename}.{extension}'

    # Azure Storage Blob takes bytes-object
    coded = base64.decodebytes(buffer.encode())

    # Create a new instance of BlobServiceClient; we will use this to create a Blob Client
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container, blob=filename_with_extension)

    # Upload
    my_content_settings = ContentSettings(content_type=content_type)
    blob_client.upload_blob(coded, blob_type="BlockBlob", overwrite=True,  content_settings=my_content_settings)

    # Get the SAS URL
    return filename_with_extension
