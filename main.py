#!usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import time
import pickle
import queue
import os
import logging
from datetime import date

# import RPi.GPIO as GPIO
from model import *
# from motor import *
from formatting import *
from preprocess import *

'''
程序运行入口
'''


def endCleanup(func):
    '''用于清理的修饰器，在程序结束后应该使用它
    '''
    def wapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            log_name = os.path.join("log", f"{date.today()}.log")
            log_format = "%(asctime)s [%(levelname)s]: %(message)s"
            date_format = "%Y/%m/%d %H:%M:%S"

            if not os.path.exists("log"):
                os.makedirs("log")

            logging.basicConfig(filename=log_name, filemode="a", level=logging.DEBUG,
                                format=log_format, datefmt=date_format, encoding="utf-8")

            # GPIO.cleanup()
            logging.info(f"程序已停止，GPIO已重置输入状态")
        return
    return wapper


@endCleanup
def main(dir_path: str):
    # 设置日志
    log_name = os.path.join("log", f"{date.today()}.log")
    log_format = "%(asctime)s [%(levelname)s]: %(message)s"
    date_format = "%Y/%m/%d %H:%M:%S"

    if not os.path.exists("log"):
        os.makedirs("log")

    logging.basicConfig(filename=log_name, filemode="a", level=logging.DEBUG,
                        format=log_format, datefmt=date_format, encoding="utf-8")
    logging.debug("程序已经开始运行")

    # 加载模型
    try:
        pca = load_model("PCA.pickle")
        svm_model = load_model("SVM.pickle")
        mlp_model = load_model("MLP.pickle")
    except:
        logging.error("模型文件缺失，程序已自动退出，请联系工作人员修理")
        raise FileNotFoundError

    # 创建队列
    q = queue.Queue(maxsize=5)

    while True:
        if not q.full():
            # 按修改时间降序排序获得文件序列表
            dirlist = os.listdir(dir_path)
            if dirlist:
                dirlist.sort(key=lambda mtime: os.path.getmtime(
                    mtime), reverse=True)
                # 向队列中存放
                q.put(getData(dirlist[-1]))
                os.remove(dirlist.pop())
            else:
                logging.debug("无待处理文件")
                time.sleep(5)
        else:
            logging.warning("操作过快，队列已满")

        # 从队列中获取数据并识别
        if not q.empty():
            data = q.get()
            slideAvg(data)
            output = pd.DataFrame(
                pca.transform(data.iloc[:, 0:-1]), index=data.index)
            svm_predict = svm_model.predict(output.iloc[:, 0:-1])
            mlp_predict = mlp_model.predict(output.iloc[:, 0:-1])
        else:
            logging.debug("队列为空")


if __name__ == '__main__':
    main("test")
