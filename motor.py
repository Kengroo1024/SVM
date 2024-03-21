#!usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import json
import tomllib
from typing import Literal

import RPi.GPIO as GPIO


class Motor:
    '''用于操作电机的类
    '''

    def __init__(self, port: dict[str, int], towards: Literal["vertical", "horizontal"], lps: float) -> None:
        """
        port是一个字典，包含电机的4个端口，字典的键为4个端口pulPlus, pulMinus, dirPlus, dirMinus
        端口的名称采用BCM编码
        """
        self._pulPlus = port["pulPlus"]
        self._pulMinus = port["pulMinus"]
        self._dirPlus = port["dirPlus"]
        self._dirMinus = port["dirMinus"]
        self.lps = lps
        with open("location.json", "r") as f:
            self._location = json.load(f)[towards]

        # GPIO相关设定
        GPIO.setmode(GPIO.BCM)
        for pin in port.values():
            GPIO.setup(pin, GPIO.OUT)

        return

    def _set_output(self, p1: bool | int, p2: bool | int, p3: bool | int, p4: bool | int) -> None:
        '''将PUL+,PUL-,DIR+,DIR-的输出按顺序指定为参数
        '''
        GPIO.output(self._pulPlus, p1)
        GPIO.output(self._pulMinus, p2)
        GPIO.output(self._dirPlus, p3)
        GPIO.output(self._dirMinus, p4)
        return

    def _up_left_wards(self, period: float) -> None:
        period /= 4
        self._set_output(1, 0, 0, 1)
        time.sleep(period)
        self._set_output(0, 1, 0, 1)
        time.sleep(period)
        self._set_output(0, 1, 1, 0)
        time.sleep(period)
        self._set_output(1, 0, 1, 0)
        time.sleep(period)
        self._location -= self.lps
        return

    def _down_right_wards(self, period: float) -> None:
        period /= 4
        self._set_output(1, 0, 1, 0)
        time.sleep(period)
        self._set_output(0, 1, 1, 0)
        time.sleep(period)
        self._set_output(0, 1, 0, 1)
        time.sleep(period)
        self._set_output(1, 0, 0, 1)
        time.sleep(period)
        self._location += self.lps
        return

    def _clean(self) -> None:
        '''clean the output of the motor to none
        '''
        self._set_output(False, False, False, False)
        return

    def auto_up_left(self, period: float) -> None:
        while self._location > 0:
            self._up_left_wards(period)
        self._clean()
        return

    def auto_down_right(self, period: float, track_length: float) -> None:
        while self._location < track_length:
            self._down_right_wards(period)
        self._clean()
        return

    def manual_control(self, towards: Literal["left", "up", "right", "down", "stop"], period: float = 10, steps: int = 0) -> None:
        """以周期period向towards前进steps步，如果towards值为stop，则停止，后面的参数都不重要，可不写
        """
        for i in range(steps):
            if towards == "stop":
                break
            elif (towards == "left") or (towards == "up"):
                self._up_left_wards(period)
            elif (towards == "right") or (towards == "down"):
                self._down_right_wards(period)
        self._clean()

    def reset_location(self):
        """将_location属性重设，一般不可使用，否则引起严重bug
        """
        self._location = 0


# 跨域电机变量
with open("config.toml", "rb") as f:
    conf = tomllib.load(f)
ver_conf = conf["motor"]["vertical"]
hor_conf = conf["motor"]["horizontal"]

vertical_motor = Motor(
    ver_conf["port"], towards="vertical", lps=ver_conf["lps"])
horizontal_motor = Motor(
    hor_conf["port"], towards="horizontal", lps=hor_conf["lps"])

if __name__ == '__main__':
    GPIO.cleanup()
