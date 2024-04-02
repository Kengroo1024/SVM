from requests import post
from pandas import DataFrame
from json import dumps
from time import sleep
import os
import shutil

from preprocess import getData
from formatting import format

while True:
    if os.listdir("raw_data"):
        format("raw_data", "data_json")
        for i in os.listdir("raw_data"):
            if os.path.isfile(os.path.join("raw_data", i)):
                os.remove(os.path.join("raw_data", i))
            else:
                shutil.rmtree(os.path.join("raw_data", i))
    if os.listdir("data_json"):
        dirlist = os.listdir("data_json")
        dirlist.sort(key=lambda x: os.path.getmtime(
            os.path.join("data_json", x)), reverse=True)
        curfile = os.path.join("data_json", dirlist[-1])

        if os.path.isfile(curfile):
            data = getData(curfile)
            json_dict = DataFrame(data["data"].tolist(),
                                  columns=data["feature_names"]).to_dict()
            a = post("http://127.0.0.1:7735/upload", json=json_dict)
            if not (a.status_code == 200):
                print("上传光谱数据失败，请检查机器是否正常运行，并重试")
                sleep(5)
                continue
            os.remove(curfile)
            del dirlist[-1]
            sleep(5)
        else:
            shutil.rmtree(curfile)
