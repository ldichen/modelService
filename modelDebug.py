"""
Author: DiChen
Date: 2024-08-15 21:07:00
LastEditors: DiChen
LastEditTime: 2024-08-24 10:08:20
"""

from ogmsServer import openModel


# Test sample data
lists = {
    "LandSlide": {
        "inputBaseTif": "./data/baseclip.tif",
        "inputPGATif": "./data/PGA.tif",
        "inputIntensityTif": "./data/intensity.tif",
    }
}

# run model and download result

taskServer = openModel.OGMSTaskAccess(modelName="地震群发滑坡概率评估预警模型")
result = taskServer.createTask(params=lists)
taskServer.downloadAllData()


# download result from url

# openModel.OGMSDownload(
#     data=[
#         {
#             "statename": "LandSlide",
#             "event": "outputPGApbtyTif",
#             "url": "http://geomodeling.njnu.edu.cn/dataTransferServer/data/251f0911-8721-4d4c-bdbb-cfe530f6a47e?pwd=",
#             "tag": "LandSlide-outputPGApbtyTif",
#             "suffix": "tif",
#             "urls": None,
#         },
#         {
#             "statename": "LandSlide",
#             "event": "outputIntensitypbtyTif",
#             "url": "http://geomodeling.njnu.edu.cn/dataTransferServer/data/c9bfac15-5355-493c-a275-09180b30571f?pwd=",
#             "tag": "LandSlide-outputIntensitypbtyTif",
#             "suffix": "tif",
#             "urls": None,
#         },
#     ]
# )
