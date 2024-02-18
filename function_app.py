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
    for blob in container_client.list_blob_names():
        logging.info(f"Found {blob}")


    # old_blob = blob_service.get_blob_client(container_name, f"{path_in}/{file_name}")
    # new_blob = blob_service.get_blob_client(container_name, f"{path_out}/{file_name}")
    # new_blob.start_copy_from_url(old_blob.url)
    # old_blob.delete_blob()
    logging.info(f"Moved {file_name} from {path_in} to {path_out}")