"""
Author: DiChen
Date: 2024-08-22 22:04:57
LastEditors: DiChen
LastEditTime: 2024-08-27 09:38:40
"""

from .base import Service
from .utils import HttpHelper
from .responseHandler import ResultUtils
from .openUtils.http_client import HttpClient
import sys
import os
import configparser
import secrets


class OGMSTask(Service):
    def __init__(
        self, ip: str, port: int, dataServer: str, dataPort: int, headers: dict
    ):
        super().__init__(ip, port)
        self.lists = {}
        self.dataServer: str = dataServer
        self.dataPort: int = dataPort
        self.headers = headers

    def configInputData(self, params: dict) -> ResultUtils:
        if not params:
            print("参数有误,请检查后重试！")
            sys.exit(1)
        for key, value in params.items():
            # 判断字典的值是否是列表
            if isinstance(value, list):
                # 遍历列表中的每一个元素
                for i, file_path in enumerate(value):
                    # 检查元素是否是以 './' 开头的字符串
                    if isinstance(file_path, str) and file_path.startswith("./"):
                        # 执行 self.uploadData 并更新列表中的元素
                        value[i] = self.uploadData(file_path)
        self.lists = params
        return ResultUtils.success()

    def uploadData(self, dataPath: str):
        res = HttpHelper.Request_post_sync(
            self.dataServer,
            self.dataPort,
            "/data",
            files={"datafile": open(dataPath, "rb")},
        )
        if res is None:
            print("上传数据出错，请联系管理员！")
            sys.exit(1)
        if res["code"] == 1:
            methodMd5 = res["data"]["id"]
            return methodMd5
        else:
            print("数据上传失败！请稍后重试！")
            sys.exit(0)


class OGMSTaskAccess(Service):
    def __init__(self, methodName: str):
        super().__init__("0", 0)
        self.outputs = {}
        self.methodId: int = None
        self.dataServer: str = None
        self.dataPort: int = None
        self.methodName = methodName
        # 创建一个配置解析器对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config_path = "./config.ini"
        if not os.path.exists(config_path):
            print("读取配置信息出错，请联系管理员！")
            sys.exit(1)
        config.read(config_path)
        self.ip = config.get("DEFAULT", "methodServer").strip()
        self.port = config.get("DEFAULT", "methodPort").strip()
        self.dataServer = config.get("DEFAULT", "dataServer").strip()
        self.dataPort = config.get("DEFAULT", "dataPort").strip()
        self.headers = {"token": f'{config.get("DEFAULT", "methodToken").strip()}'}
        if not (
            self.ip or self.port or self.dataServer or self.dataPort or self.headers
        ):
            print("读取配置信息出错，请联系管理员！")
            sys.exit(1)
        # TODO: 检测服务情况
        self.checkMethod(methodName=methodName)

    def checkMethod(self, methodName: str):
        if not methodName:
            print("方法名不能为空")
            sys.exit(1)
        # res = HttpClient.get_sync(
        #     url=f"http://{self.ip}:{self.port}/renren-fast/container/method/infoByName/{methodName}",
        #     headers=self.headers,
        # )
        res = HttpHelper.Request_get_sync(
            self.ip,
            self.port,
            "/renren-fast/container/method/infoByName/" + methodName,
            headers=self.headers,
        )
        if res is None:
            print("方法不存在，请联系管理员！")
            sys.exit(1)
        else:
            if res["code"] == 0:
                self.methodId = res["method"]["id"]
            else:
                print("方法不存在，请联系管理员！")
                sys.exit(1)

    def subscribeTask(self, task: OGMSTask) -> ResultUtils:
        res = HttpHelper.Request_post_json_sync(
            self.ip,
            self.port,
            f"/renren-fast/container/method/invoke/{self.methodId}",
            task.lists,
            headers=self.headers,
        )
        if res is None:
            print("方法调用失败，请重试！")
            sys.exit(1)
        else:
            if res["code"] == 0:
                if res["output"] is None:
                    return ResultUtils.error("计算有误，请检查后重试！")
                for key in res["output"]:
                    res["output"][key] = [
                        f"http://{self.dataServer}:{self.dataPort}/data/" + val
                        for val in res["output"][key]
                    ]

                self.outputs = res["output"]
                print(self.outputs)
                return ResultUtils.success(data=self.outputs)
            print("方法返回数据缺失，请重试！")
            sys.exit(1)

    def createTask(self, params: dict) -> ResultUtils:
        if not params:
            print("参数有误,请检查后重试！")
            sys.exit(1)
        task = OGMSTask(
            self.ip, self.port, self.dataServer, self.dataPort, self.headers
        )
        c = task.configInputData(params)
        if c.code != 1:
            return c
        return self.subscribeTask(task)

    def downloadAllData(self) -> list:
        def process_filename(filename):
            # 查找点的位置
            dot_positions = [pos for pos, char in enumerate(filename) if char == "."]

            # 判断是否有两个或更多的点
            if len(dot_positions) >= 2:
                # 保留从开始到第二个点之前的部分
                result = filename[: dot_positions[1]]
            else:
                # 如果点少于两个，保留原始文件名
                result = filename

            return result

        downloadFilesNum = 0
        downlaodedFilesNum = 0
        if not self.outputs:
            print("没有可下载的数据")
            return False

        for event in self.outputs:
            for index, url in enumerate(self.outputs[event]):
                downloadFilesNum = downloadFilesNum + 1
                content, content_disposition = HttpHelper.Request_get_url_sync(url)
                # 从Content-Disposition头中提取文件名
                filename = content_disposition.split("fileName=")[-1].strip('"')
                filename = process_filename(filename)
                couter = 1

                if content:
                    s_id = secrets.token_hex(8)
                    file_path = (
                        "./data/" + self.methodName + "_" + s_id + "/" + filename
                    )
                    dir_path = os.path.dirname(file_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    while os.path.exists(file_path):
                        name, ext = os.path.splitext(filename)
                        filename = f"{name}_{counter}.{ext}"
                        file_path = (
                            "./data/" + self.methodName + "_" + s_id + "/" + filename
                        )
                        counter += 1

                    with open(file_path, "wb") as f:
                        f.write(content)
                    self.outputs[event][index] = file_path
                    print(f"Downloaded {filename}")
                    downlaodedFilesNum = downlaodedFilesNum + 1
                else:
                    print(f"Failed to download {url}")
        if downlaodedFilesNum == 0:
            print("Failed to download files")
            sys.exit(1)
        if downloadFilesNum == downlaodedFilesNum:
            print("All files downloaded successfully")
            return self.outputs
        else:
            print("Failed to download some files")
            return self.outputs


class OGMSDownload:
    def __init__(self, data: dict):
        self.outputs = data

        def process_filename(filename):
            # 查找点的位置
            dot_positions = [pos for pos, char in enumerate(filename) if char == "."]

            # 判断是否有两个或更多的点
            if len(dot_positions) >= 2:
                # 保留从开始到第二个点之前的部分
                result = filename[: dot_positions[1]]
            else:
                # 如果点少于两个，保留原始文件名
                result = filename

            return result

        downloadFilesNum = 0
        downlaodedFilesNum = 0
        if not self.outputs:
            print("没有可下载的数据")
            return False

        for event in self.outputs:
            for index, url in enumerate(self.outputs[event]):
                downloadFilesNum = downloadFilesNum + 1
                content, content_disposition = HttpHelper.Request_get_url_sync(url)
                # 从Content-Disposition头中提取文件名
                filename = content_disposition.split("fileName=")[-1].strip('"')
                filename = process_filename(filename)
                couter = 1

                if content:
                    s_id = secrets.token_hex(8)
                    file_path = (
                        "./data/" + self.methodName + "_" + s_id + "/" + filename
                    )
                    dir_path = os.path.dirname(file_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    while os.path.exists(file_path):
                        name, ext = os.path.splitext(filename)
                        filename = f"{name}_{counter}.{ext}"
                        file_path = (
                            "./data/" + self.methodName + "_" + s_id + "/" + filename
                        )
                        counter += 1

                    with open(file_path, "wb") as f:
                        f.write(content)
                    self.outputs[event][index] = file_path
                    print(f"Downloaded {filename}")
                    downlaodedFilesNum = downlaodedFilesNum + 1
                else:
                    print(f"Failed to download {url}")
        if downlaodedFilesNum == 0:
            print("Failed to download files")
            sys.exit(1)
        if downloadFilesNum == downlaodedFilesNum:
            print("All files downloaded successfully")
            return self.outputs
        else:
            print("Failed to download some files")
            return self.outputs
