"""
Author: DiChen
Date: 2024-09-07 09:26:00
LastEditors: DiChen
LastEditTime: 2024-09-11 18:27:36
"""

"""
Author: DiChen
Date: 2024-09-07 09:26:00
LastEditors: DiChen
LastEditTime: 2024-09-07 09:27:19
"""

from ogmsServer2 import openModel

# Test sample data
lists = {
    "LandSlide": {
        "inputBaseTif": "./data/baseclip.tif",
        "inputPGATif": "./data/PGA.tif",
        "inputIntensityTif": "./data/intensity.tif",
    }
}

# run model and download result

taskServer = openModel.OGMSAccess(
    modelName="地震群发滑坡概率评估预警模型",
    token="6U3O1Sy5696I5ryJFaYCYVjcIV7rhd1MKK0QGX9A7zafogi8xTdvejl6ISUP1lEs",
)
result = taskServer.createTask(params=lists)
taskServer.downloadAllData()
