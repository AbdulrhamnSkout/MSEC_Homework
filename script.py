import os
import uuid
import shutil

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
connect_str_1 = "DefaultEndpointsProtocol=https;AccountName=abdsta1;AccountKey=mVdfL4lcPWqwq55QopypK0xiN88jna8rPvSz1aiPRlq4ALfxhBU0yMgohiU+YmgKifo09pBWg+UY2kWVs09nbA==;EndpointSuffix=core.windows.net"
connect_str_2="DefaultEndpointsProtocol=https;AccountName=abdstb2;AccountKey=7U5RFj25fK0rwJvMC3/BUsLG6qx2v+45FJ421qXdWVMVNRZ51V4ayMAUB1iBAVZzomoSh7DPhS2AqD1kYYpTqQ==;EndpointSuffix=core.windows.net"
first_container_name="upload-container"
second_container_name="donwload-container"



def download_all_blobs_in_container(first_container_name,connect_str):
    os.mkdir("./download")
    blob_service_client =  BlobServiceClient.from_connection_string(connect_str)
    my_container = blob_service_client.get_container_client(first_container_name)
    my_blobs =my_container.list_blobs()
    for blob in my_blobs:
        print(blob.name)
        bytes = my_container.get_blob_client(blob).download_blob().readall()
        save_blob(blob.name, bytes)


def save_blob(file_name,file_content):
    # Get full path to the file
    download_file_path = os.path.join("C:/Users/abd/Desktop/script/download", file_name)
 
    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
 
    with open(download_file_path, "wb") as file:
      file.write(file_content)


def upload_blob(path,name,connect_str):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    #Create name for the container
    container_name = name
    # Create the container
    container_client = blob_service_client.create_container(container_name)
    #upload blob
    for file in os.listdir(path):
        if file.endswith(".txt"):
            blob_client = blob_service_client.get_blob_client(container=container_name,blob=file)
            file_path = os.path.join(path,file)
            print(f'upload {file}')
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)


def create_blob():
    local_path = "./data"
    os.mkdir(local_path)
    for i in range(100):
        local_file_name =f'blob_{i}.txt'
        file_path = os.path.join(local_path, local_file_name)
        file = open(file_path, 'w')
        file.write("Hello, World!")
        file.close()


try:  
    create_blob()
    
    upload_blob("./data",first_container_name,connect_str_1)
        
    download_all_blobs_in_container(first_container_name,connect_str_1)
    
    upload_blob("./download",second_container_name,connect_str_2)
   
    shutil.rmtree("./download")
    shutil.rmtree("./data")

except Exception as ex:
    print('Exception:')
    print(ex)
