"""
Author: DiChen
Date: 2024-09-06 15:14:57
LastEditors: DiChen
LastEditTime: 2024-09-06 17:05:36
"""

from .base import Service
from openUtils.stateManager import StateManager
from openUtils.http_client import HttpClient
import sys
import urllib.parse


class OGMSTask:
    def __init__(self):
        pass


class OGMSAccess(Service):
    def __init__(self, modelName: str):
        super().__init__()
        if not modelName or not modelName.strip():
            raise ValueError("Model name cannot be None or empty, please check!")
        self.modelName = modelName
        self.checkModel(modelName=modelName)

    def checkModel(self, modelName: str):
        if not modelName or not modelName.strip():
            raise ValueError("Model name cannot be None or empty, please check!")
        encode2url = urllib.parse.quote(modelName)
        res = HttpClient.get(
            self.portalUrl + "/computableModel/ModelInfo_name/" + encode2url
        )
        pass

    def createTask(self, params: dict):
        pass

    def downloadAllData(self):
        pass
