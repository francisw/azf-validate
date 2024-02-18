import azure.functions as func
from azure.identity import DefaultAzureCredential
import json
from azure.storage.blob import BlobServiceClient
from pprint import pprint
import logging

app = func.FunctionApp()

connection_string = "DefaultEndpointsProtocol=https;AccountName=azfvalidate;AccountKey=E9pr7kKL+rNEr8jWqr4eZCY58JNMqM4rYTF6pX2ApeGQQ3rkJqmhHINPQm9i0HxDkkh1eVyW+W5P+AStjP9W3w==;EndpointSuffix=core.windows.net"

account_url = "https://azfvalidate.blob.core.windows.net"

container_name = "validate"
path_in = "in"
path_out = "out"

@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="myblob", path="validate/in",
                               connection="AzureWebJobsStorage") 
def xml_validate(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}" 
                f"Blob Size: {myblob.length} bytes")
    file_name = myblob.name.split("/")[-1]
    logging.info(f"File Name: {file_name}")

   # default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    for blob in container_client.list_blobs():
        logging.info(f"Found {blob.name}")

    # blob_client = container_client.get_blob_client(f"{path_out}/{file_name}")
    # blob_client.start_copy_from_url(f"{account_url}/{container_name}/{path_out}/{file_name}", requires_sync = True )
    
    # old_blob = blob_service_client.get_blob_client(container_name, f"{path_in}/{file_name}")
    new_blob = blob_service_client.get_blob_client(container_name, f"{path_out}/{file_name}")
    theData = myblob.read()
    new_blob.upload_blob(theData)
    # old_blob.delete_blob()
    for blob in container_client.list_blobs():
        logging.info(f"Found {blob.name}")

    logging.info(f"Moved {file_name} from {path_in} to {path_out}")