"""
Author: DiChen
Date: 2024-09-06 15:22:20
LastEditors: DiChen
LastEditTime: 2024-09-09 19:05:17
"""

"""
Author: DiChen
Date: 2024-09-06 15:22:20
LastEditors: DiChen
LastEditTime: 2024-09-08 20:15:23
"""

"""
Author: DiChen
Date: 2024-09-06 15:22:20
LastEditors: DiChen
LastEditTime: 2024-09-06 15:39:59
"""

import sys
import configparser
import os


class Service:
    def __init__(self, token: str = None):
        self.token: str = token
        # 创建一个配置解析器对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config_path = "./config2.ini"
        if not os.path.exists(config_path):
            print("读取配置文件有误，请联系管理员！")
            sys.exit(1)
        config.read(config_path)
        self.portalUrl = config.get("DEFAULT", "basePortalUrl").strip()
        self.managerUrl = config.get("DEFAULT", "baseManagerUrl").strip()
        self.dataUrl = config.get("DEFAULT", "baseDataUrl").strip()
        self.modelToken = config.get("DEFAULT", "modelToken").strip()
        if not (self.portalUrl or self.managerUrl or self.dataUrl or self.modelToken):
            print("读取配置文件有误，请联系管理员！")
            sys.exit(1)
