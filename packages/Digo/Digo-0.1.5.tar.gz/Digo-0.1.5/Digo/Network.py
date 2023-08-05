import requests
from Digo import SystemMetrics
import sys
import os
import json
import random
import numpy as np
from PIL import Image
import string
# from Digo.AzureCloud import AzureCloudService
from collections import OrderedDict

from Digo.Utils import FILETYPE

DIGO_WEB = 'http://app.digo.ai:7777/digo-server'
# DIGO_WEB = 'http://digger.works:7777/digo-server'


# azure_cloud_service = AzureCloudService()
imageLogStep = 0
modelFileStep = 0


def login(api_key, workspace_name):
    conn = requests.get(DIGO_WEB + "/SignInUseAPI",
                        params={'api_key': api_key, 'workspace_name': workspace_name})

    return conn.json()


def updateLog(api_key , account_id, project_id, experiment_id, log):
    conn = requests.post(DIGO_WEB + "/UpdateLog", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'log': log, 'system_metrics': SystemMetrics.getSystemMetrics()})


def updatePrintLog(api_key, account_id, project_id, experiment_id, log):
    conn = requests.post(DIGO_WEB + "/UpdatePrintLog", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'print_log': log})


def updateHyperParameter(api_key, account_id, project_id, experiment_id, hyper_parameter):
    conn = requests.post(DIGO_WEB + "/UpdateHyperParameter", params={
        'api_key': api_key, 'account_id': account_id,'project_id':project_id, 'experiment_id': experiment_id, 'hyper_parameter': hyper_parameter})

def updateExperimentState(api_key, account_id,experiment_id, project_id, state):
    conn = requests.post(DIGO_WEB + "/UpdateExperimentState", params={
        'api_key': api_key, 'account_id': account_id, 'experiment_id': experiment_id,'project_id':project_id, 'experiment_state':state})


def upload_file_to_main(file, api_key, account_id, file_type, workspace_name, project_name, experiment_name):
    # DIGO_WEB
    conn = requests.post(DIGO_WEB + "/UploadFileForModule",
                         params={'api_key': api_key, 'account_id': account_id, 'file_type':file_type,
                                 'workspace_name': workspace_name, 'project_name': project_name, 'experiment_name': experiment_name},
                         files={"file":file})
    # print(conn.json())
    return conn.json()["file_index"]


def uploadModelFile(api_key, account_id,project_id, experiment_name, sas_token, container_name, project_name, experiment_id, model_path, workspace_name):
    global modelFileStep
    current_dir = os.getcwd()
    origin_file_name = model_path.split('/')[-1]
    file_name = str(modelFileStep) + "_" + origin_file_name

    if model_path.startswith('/'):
        full_path = current_dir + model_path
    else:
        full_path = current_dir + os.sep + model_path

    convert_full_path = full_path.split(origin_file_name)[0] + file_name

    os.rename(full_path, convert_full_path)

    # print(convert_full_path)

    blob_id = upload_file_to_main(file=open(convert_full_path, 'rb'), account_id= account_id, api_key=api_key, file_type=FILETYPE.MODEL.name,
                                  workspace_name=workspace_name, project_name=project_name, experiment_name=experiment_name)

    model_blob = OrderedDict()
    model_blob[file_name] = blob_id
    os.rename(convert_full_path, full_path)
    conn = requests.post(DIGO_WEB + "/ModelFileAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'model_blob': json.dumps(model_blob)})
    modelFileStep +=1

def uploadSourceCode(api_key, account_id, project_id, experiment_name, sas_token, container_name, project_name, experiment_id,
                     workspace_name):

    local_file_name = sys.argv[0]
    directory, file_name = os.path.split(local_file_name)
    current_dir = os.getcwd()
    full_path = current_dir + os.sep + file_name

    blob_id = upload_file_to_main(file=open(local_file_name, 'rb'), api_key=api_key, account_id=account_id, file_type=FILETYPE.SOURCE.name,
                                  workspace_name=workspace_name, project_name=project_name, experiment_name=experiment_name)

    requests.post(DIGO_WEB + "/UpdateRunPath", params={
        'api_key': api_key, 'account_id':account_id, 'experiment_id':experiment_id, 'run_path': full_path})
    requests.post(DIGO_WEB + "/SourceCodeAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'azure_blob_id': blob_id})


def uploadRequirementsFile(api_key, account_id, project_id, experiment_id, requirements):
    conn = requests.post(DIGO_WEB + "/UploadRequirements", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'requirements': requirements})


def uploadImageLog(api_key, account_id, sas_token, project_id, experiment_id, container_name, project_name, experiment_name, imageLog, workspace_name):
    global imageLogStep

    local_file_name = sys.argv[0]
    directory, file_name = os.path.split(local_file_name)
    current_dir = os.getcwd()
    full_path = current_dir + os.sep + local_file_name
    # print(full_path)

    result_image_log = OrderedDict()

    if os.path.isdir(current_dir+ os.sep + 'temp') is False :
        os.mkdir(current_dir+ os.sep + 'temp')


    for key in imageLog:
        if type(imageLog[key]) is np.ndarray:
            image_data = Image.fromarray(imageLog[key])
        else:
            image_data = imageLog[key]
        image_name: str = key + "_" + str(imageLogStep)
        image_data.save(current_dir+ os.sep + 'temp' + os.sep + image_name + '.png', 'PNG')
        full_path = current_dir + os.sep + 'temp' + os.sep + image_name +'.png'
        result_image_log[key] = upload_file_to_main(file=open(full_path, 'rb'), api_key=api_key, account_id=account_id, file_type=FILETYPE.IMAGE.name,
                                                    workspace_name=workspace_name, project_name=project_name, experiment_name=experiment_name)
        # azure_cloud_service.upload_image(full_path, image_name+'.png', sas_token, container_name, project_name, experiment_name, experiment_id)
        os.remove(current_dir + os.sep + 'temp' + os.sep + image_name + '.png')

    conn = requests.post(DIGO_WEB + "/ImageAzureUpdateComplete", params={
        'api_key': api_key, 'account_id': account_id, 'project_id':project_id, 'experiment_id': experiment_id, 'image_blob_id': json.dumps(result_image_log)})

    imageLogStep += 1


def updateExperimentFinished(api_key, account_id, experiment_id, state):
    conn = requests.post(DIGO_WEB + "/UpdateExperimentFinished", params={
        'api_key': api_key, 'account_email': account_id, 'experiment_index': experiment_id, 'experiment_state': state})
