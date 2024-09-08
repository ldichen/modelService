"""
Author: DiChen
Date: 2024-09-06 15:14:57
LastEditors: DiChen
LastEditTime: 2024-09-07 00:16:30
"""

from g_imports import *


class OGMSTask(Service):
    def __init__(self, params: dict):
        super().__init__()
        self.status: None | int = None
        PV.v_empty(params, "Params")
        # 对输入的参数进行校验、文件上传等操作

    def wait4Status(self, timeout: int = 7200):
        try:
            start_time = time.time()
            stateManager = StateManager()
            stateManager.checkInputStatus(PV.v_status(self._refresh()))
            while stateManager.getState != 0b100:
                stateManager.checkInputStatus(PV.v_status(self._refresh()))
                if time.time() - start_time > timeout:
                    raise calTimeoutError()
                time.sleep(3)
        except NotValueError or modelStatusError as e:
            print(e)
            exit(1)

    ########################private################################
    def _uploadData(self, dataPath: str):
        pass

    def _refresh(self):
        PV.v_empty(self.modelSign, "Model sign")
        res = HttpClient.hander_response(
            HttpClient.post_sync(
                url=self.managerUrl + C.REFRESH_RECORD, data=self.modelSign
            )
        ).get("json", {})
        if res.get("code") == 1:
            if res.get("data").get("status") != 2:
                return res.get("data").get("status")
            else:
                hasValue = False
                for output in res["data"]["outputs"]:
                    if output.get("url") is not None and output.get("url") != "":
                        url = output.get("url")
                        updated_url = url.replace(
                            "http://112.4.132.6:8083",
                            "http://geomodeling.njnu.edu.cn/dataTransferServer",
                        )
                        output["url"] = updated_url
                        hasValue = True
                if hasValue is False:
                    return -1
                for output in res["data"]["outputs"]:
                    if "[" in output.get("url"):
                        output["multiple"] = True
                self.outputs = res["data"]["outputs"]
                return 2
        return -2


class OGMSAccess(Service):
    def __init__(self, modelName: str, token: str | None = None):
        super().__init__(token=token)
        PV.v_empty(modelName, "Model name")
        self.modelName = modelName
        self.subsribeList = {}
        self.outputs = []
        if self._checkModelService(pid=self._checkModel(modelName=modelName)):
            print("Model service is ready!")
        else:
            print("Model service is not ready, please try again later!")
            exit(1)

    def createTask(self, params: dict):
        PV.v_empty(params, "Params")
        task = OGMSTask(self.subsribeList)
        if task.validate(params):
            self._subscribeTask()
        result = task.wait4Status()
        pass

    def downloadAllData(self):
        pass

    ########################private################################
    def _checkModel(self, modelName: str):
        PV.v_empty(modelName, "Model name")
        res = (
            HttpClient.hander_response(
                HttpClient.get_sync(
                    self.portalUrl + C.CHECK_MODEL + urllib.parse.quote(modelName)
                )
            )
            .get("json", {})
            .get("data", {})
        )
        if res.get("md5"):
            self._checkModelService(pid=res.get("pid"))
            self.subsribeList = MdlUtils.resolveMDL(res.get("mdl"))
            return res.get("pid")
        return 0

    def _checkModelService(self, pid: str):
        PV.v_empty(pid, "Model pid")
        if (
            HttpClient.hander_response(
                HttpClient.get_sync(self.managerUrl + C.CHECK_MODEL_SERVICE + pid)
            )
            .get("json", {})
            .get("data", {})
            == True
        ):
            return 1
        return 0

    def _subscribeTask(self):
        res = HttpClient.post_sync(self.managerUrl + C.INVOKE_MODEL, self.subsribeList)
        pass
