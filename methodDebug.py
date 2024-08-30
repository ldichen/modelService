"""
Author: DiChen
Date: 2024-08-27 10:31:06
LastEditors: DiChen
LastEditTime: 2024-08-29 16:04:49
"""

"""
Author: DiChen
Date: 2024-08-27 10:31:06
LastEditors: DiChen
LastEditTime: 2024-08-29 14:44:30
"""

"""
Author: DiChen
Date: 2024-08-27 10:31:06
LastEditors: DiChen
LastEditTime: 2024-08-29 14:33:33
"""

"""
Author: DiChen
Date: 2024-08-27 10:31:06
LastEditors: DiChen
LastEditTime: 2024-08-27 10:32:29
"""

from ogmsServer import openMethod

lists = {
    "val0": "./data/small_sample.tiff",
    "val1": "",
    "val2": 1,
    "val3": None,
    "val4": "true",
    "val5": None,
    "val6": "false",
}
lists2 = {
    "val0": [
        "./data/small_sample.tiff",
        "./data/small_sample.tiff",
    ],
    "val1": "Rook",
    "val2": "result",
}


taskServer = openMethod.OGMSTaskAccess(methodName="ImageAutocorrelation")
result = taskServer.createTask(params=lists2)
info = taskServer.downloadAllData()
print(info)
