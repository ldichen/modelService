"""
Author: DiChen
Date: 2024-08-12 14:47:40
LastEditors: DiChen
LastEditTime: 2024-09-09 20:24:00
"""

"""
Author: DiChen
Date: 2024-08-12 14:47:40
LastEditors: DiChen
LastEditTime: 2024-09-06 00:46:33
"""

from .utils import HttpHelper


class Service:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def getBaseURL(self) -> str:
        return "http://" + self.ip + ":" + str(self.port) + "/"

    def connect(self) -> bool:
        strData = HttpHelper.Request_get_str_sync(self.ip, self.port, "/ping")
        if strData == "OK":
            return True
        else:
            return False
