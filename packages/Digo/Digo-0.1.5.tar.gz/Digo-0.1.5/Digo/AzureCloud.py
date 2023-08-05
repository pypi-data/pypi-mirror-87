# from azure.storage.blob import BlobServiceClient
# from azure.storage.blob import ContainerClient

# import os
# import requests
# import random
# import string


# # server parameter
# DIGO_WEB = 'http://digo.ai:7777/digo-server'
# # DIGO_WEB = 'http://localhost:8080/'


# class AzureCloudService:

#     def upload_source_file(self,
#                            full_path_to_file,
#                            file_name,
#                            sas_token,
#                            container_name,
#                            project_name,
#                            experiment_name,
#                            experiment_id):

#         return self._save_blob_to_cloud(full_path_to_file,
#                                         file_name,
#                                         'Source Code',
#                                         sas_token,
#                                         container_name,
#                                         project_name,
#                                         experiment_name,
#                                         experiment_id)

#     def upload_model_file(self,
#                           full_path_to_file,
#                           file_name,
#                           sas_token,
#                           container_name,
#                           project_name,
#                           experiment_name,
#                           experiment_id):

#         return self._save_blob_to_cloud(full_path_to_file,
#                                         file_name,
#                                         'Model',
#                                         sas_token,
#                                         container_name,
#                                         project_name,
#                                         experiment_name,
#                                         experiment_id)

#     def upload_image(self,
#                      full_path_to_file,
#                      file_name,
#                      sas_token,
#                      container_name,
#                      project_name,
#                      experiment_name,
#                      experiment_id):

#         return self._save_blob_to_cloud(full_path_to_file,
#                                         file_name,
#                                         'Image',
#                                         sas_token,
#                                         container_name,
#                                         project_name,
#                                         experiment_name,
#                                         experiment_id)

#     def _upload_to_cloud(self,
#                          data,
#                          file_name,
#                          file_type,
#                          project_name,
#                          experiment_name,
#                          blob_service_client: BlobServiceClient,
#                          container_name: str):

#         random_pool = string.ascii_letters + string.digits
#         random_len = 8
#         random_str = ''
#         for _ in range(random_len):
#             random_str += random.choice(random_pool)

#         file_dir, temp = os.path.split(data.name)
#         save_name = project_name + os.path.sep + experiment_name + os.path.sep

#         if file_type == 'Source Code':
#             save_name = save_name + 'source' + os.sep + file_name
#         elif file_type == 'Image':
#             save_name = save_name + 'images' + os.sep + file_name
#         elif file_type == 'Model':
#             save_name = save_name + 'model' + os.sep + file_name
#         else:
#             raise Exception('Invalid File Type!!!')

#         container_name = container_name.strip()

#         # print('Uploading... ' + save_name)
#         blob_client = blob_service_client.get_blob_client(blob=save_name)
#         blob_client.upload_blob(data, overwrite=True)
#         # print('Upload Succeed!!')

#     def _build_connection_string(self,
#                                  account_name,
#                                  account_key):
#         connection_string = 'DefaultEndpointsProtocol=https' + ';'\
#                             'AccountName=' + account_name + ';' \
#                             'AccountKey=' + account_key + ';' \
#                             'EndpointSuffix=core.windows.net'

#         return connection_string

#     def _save_blob_to_cloud(self,
#                             full_path_to_file,
#                             file_name,
#                             file_type,
#                             sas_token,
#                             container_name,
#                             project_name,
#                             experiment_name,
#                             experiment_id):

#         with open(full_path_to_file, 'rb') as file:
#             # later: use 'isinstance' to check instance.
#             conn: requests.Response = None

#             file_size = os.path.getsize(file.name)

#             if file_size == 0:
#                 raise Exception('No File Detected!!!')

#             params = {'container_name': container_name,
#                       'project_name': project_name,
#                       'experiment_name': experiment_name,
#                       'experiment_id': experiment_id,
#                       'file_name': file_name,
#                       'file_size': file_size,
#                       'file_type': file_type}

#             conn = requests.get(
#                 DIGO_WEB + "/CheckAzureCloud", params=params)

#             json_data = conn.json()

#             # print(conn.url)

#             # Response from server
#             if json_data['code'] == 0:
#                 blob_service_client = ContainerClient.from_container_url(
#                     container_url="https://digocloud.blob.core.windows.net/"+container_name,
#                     credential=sas_token
#                 )

#                 # BlobServiceClient.from_connection_string(connection_string)

#                 self._upload_to_cloud(file,
#                                       file_name,
#                                       file_type,
#                                       project_name,
#                                       experiment_name,
#                                       blob_service_client,
#                                       container_name,)

#                 return json_data['azure_blob_id']

#             elif json_data['code'] == -200:
#                 raise Exception('Not Enough Storage Left!!!')
