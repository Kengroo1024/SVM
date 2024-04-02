#!usr/bin/env python
# -*- coding: UTF-8 -*-
import tomllib
import json
import time
import queue
import os
import sys
import logging
from datetime import date

import RPi.GPIO as GPIO
from model import *
from motor import Motor
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
        except ValueError or KeyError or TypeError:
            logging.error("配置文件不合法，程序已退出")
        except KeyboardInterrupt:
            logging.info("已通过键盘退出程序")
        except FileNotFoundError:
            logging.error("没有找到依赖文件，程序已退出")
        except SystemExit:
            logging.info("已自动退出清理程序")
        finally:
            global vertical_motor, horizontal_motor
            location = {
                "vertical": vertical_motor._location,
                "horizontal": horizontal_motor._location
            }

            with open("location.json", "w") as f:
                json.dump(location, f)

            # log_name = os.path.join("log", f"{date.today()}.log")
            # log_format = "%(asctime)s [%(levelname)s]: %(message)s"
            # date_format = "%Y/%m/%d %H:%M:%S"
            # if not os.path.exists("log"):
            #     os.makedirs("log")
            # logging.basicConfig(filename=log_name, filemode="a", level=logging.DEBUG,
            #                     format=log_format, datefmt=date_format, encoding="utf-8")
            GPIO.cleanup()
            logging.info("GPIO已重置输入状态")
        return
    return wapper


@endCleanup
def main():
    with open("config.toml", "rb") as cf:
        config = tomllib.load(cf)
    # 设置日志
    log_name = os.path.join(config['path']['log'], f"{date.today()}.log")
    log_format = "%(asctime)s [%(levelname)s]: %(message)s"
    date_format = "%Y/%m/%d %H:%M:%S"

    if not os.path.exists(config['path']['log']):
        os.makedirs(config['path']['log'])

    match config["log_level"]:
        case "info":
            level = logging.INFO
        case "debug":
            level = logging.DEBUG
        case "error":
            level = logging.ERROR
        case _:
            raise ValueError("配置文件不合法")

    logging.basicConfig(filename=log_name, filemode="a", level=level,
                        format=log_format, datefmt=date_format, encoding="utf-8")
    # 加载模型

    logging.debug("程序已经开始运行")
    # 创建队列
    q = queue.Queue(maxsize=5)
    # 获取模型文件
    pca = load_model("PCA.pickle")
    if config["method"] == "svm":
        svm_model = load_model("SVM.pickle")
    elif config["method"] == "mlp":
        mlp_model = load_model("MLP.pickle")
    else:
        raise ValueError("配置文件不合法")

    with open("config.toml", "rb") as f:
        conf = tomllib.load(f)
    ver_conf = conf["motor"]["vertical"]
    hor_conf = conf["motor"]["horizontal"]

    global vertical_motor, horizontal_motor
    vertical_motor = Motor(
        ver_conf["port"], towards="vertical", lps=ver_conf["lps"])
    horizontal_motor = Motor(
        hor_conf["port"], towards="horizontal", lps=hor_conf["lps"])

    vertical_motor.auto_up_left(config["motor"]["vertical"]["period"])
    horizontal_motor.auto_up_left(
        config["motor"]["horizontal"]["period"])
    # 自动关机计数变量
    count = 0
    while True:
        if not q.full():
            # 按修改时间降序排序获得文件列表
            dirlist = os.listdir(config['path']['new_file_dir'])
            if dirlist:
                dirlist.sort(key=lambda mtime: os.path.getmtime(
                    os.path.join(config['path']['new_file_dir'], mtime)),
                    reverse=True)
                # 向队列中存放
                q.put(getData(os.path.join(
                    config['path']['new_file_dir'], dirlist[-1])))
                os.remove(os.path.join(
                    config['path']['new_file_dir'], dirlist.pop()))
            else:
                logging.debug("无待处理文件")
        else:
            logging.warning("操作过快，队列已满")

        # 从队列中获取数据并识别
        if not q.empty():
            count = 0
            data = q.get()
            slideAvg(data)
            output = pca.transform(data["data"][:, 0:-1])
            if config["method"] == "svm":
                predict = svm_model.predict(output)[0]
            elif config["method"] == "mlp":
                predict = mlp_model.predict(output)[0]

            logging.info(f"获取的预测值为{'塑料' if predict else '非塑料'}")

            if predict:
                vertical_motor.auto_down_right(
                    period=config["motor"]["vertical"]["period"],
                    track_length=config["motor"]["vertical"]["track_length"]
                )
                horizontal_motor.auto_down_right(
                    period=config["motor"]["horizontal"]["period"],
                    track_length=config["motor"]["horizontal"]["track_length"]
                )
                vertical_motor.auto_up_left(
                    period=config["motor"]["vertical"]["period"]
                )
                horizontal_motor.auto_up_left(
                    period=config["motor"]["horizontal"]["period"]
                )
            else:
                time.sleep(5)
        else:
            logging.debug("队列为空")
            time.sleep(5)
            if config["autoshutdown"]:
                count += 1
                if count == 120:
                    sys.exit()


if __name__ == '__main__':
    main()
