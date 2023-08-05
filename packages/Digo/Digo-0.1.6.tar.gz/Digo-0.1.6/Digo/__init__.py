# __init__.py
# Copyright (C) 2020 (support@digger.works) and digger


__author__ = 'DiggerWorks'
__email__ = 'support@digger.works'
__version__ = '0.1.6'

from Digo import DigoCore
from Digo import Error
from Digo import ExceptionHandler
import json
import argparse

core = None


def init(api_key: str, workspace_name: str, project_name: str, isDev:bool = False):
    global core
    core = DigoCore.Core(
        api=api_key, workspace_name=workspace_name, project_name=project_name, isDev=isDev)
    if isDev == True:
            DigoCore.Network.DIGO_WEB = "http://digger.works:7777/digo-server"
            core.DIGO_WEB = "http://digger.works:7777/digo-server"

def log(log):
    if core is None:
        raise Error.NotFoundCore
    core.send_log(log)


def imageLog(log):
    if type(log) == dict:
        core.imageLog(log)
    else:
        raise Error.InvalidType

def upload_test(file):
    core.upload_test(file)

def uploadModel(model_path):
    core.uploadModel(model_path)

def setParameter(hyper_parameter):
    if core is None:
        raise Error.NotFoundCore

    if type(hyper_parameter) == argparse.ArgumentParser:
        parameter = vars(hyper_parameter.parse_args())
        print(json.dumps(parameter))
        core.send_hyper_parameter(json.dumps(parameter))
    elif type(hyper_parameter) == dict:
        core.send_hyper_parameter(json.dumps(parameter))
    else:
        raise Error.InvalidType


def printf(log):
    if core is None:
        raise Error.NotFoundCore

    print(log)
    core.printLog(log)
