"""
Author: DiChen
Date: 2024-08-27 10:31:06
LastEditors: DiChen
LastEditTime: 2024-08-29 16:04:49
"""

from ogmsServer import openMethod

lists = {
    "val0": ["./data/small_sample.tiff"],
    "val1": "test",
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
    "val2": "test",
}


taskServer = openMethod.OGMSTaskAccess(methodName="BreachDepressionsLeastCost")
result = taskServer.createTask(params=lists)
info = taskServer.downloadAllData()
print(info)
