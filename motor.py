#!usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import RPi.GPIO as GPIO
import json
from typing import Literal


class Motor:
    '''用于操作电机的类
    '''

    def __init__(self, port: dict[str, int], towards: Literal["vertical", "horizontal"], lps: float) -> None:
        """
        port是一个字典，包含电机的4个端口，字典的键为4个端口pulPlus, pulMinus, dirPlus, dirMinus
        端口的名称采用BCM编码
        """
        self.pulPlus = port["pulPlus"]
        self.pulMinus = port["pulMinus"]
        self.dirPlus = port["dirPlus"]
        self.dirMinus = port["dirMinus"]
        self.lps = lps
        with open("location.json", "r") as f:
            self.location = json.load(f)[towards]

        # GPIO相关设定
        GPIO.setmode(GPIO.BCM)
        for pin in port.values():
            GPIO.setup(pin, GPIO.OUT)

        return

    def set_output(self, p1: bool | int, p2: bool | int, p3: bool | int, p4: bool | int) -> None:
        '''将PUL+,PUL-,DIR+,DIR-的输出按顺序指定为参数
        '''
        GPIO.output(self.pulPlus, p1)
        GPIO.output(self.pulMinus, p2)
        GPIO.output(self.dirPlus, p3)
        GPIO.output(self.dirMinus, p4)
        return

    def up_left_wards(self, period: float) -> None:
        period /= 4
        self.set_output(1, 0, 0, 1)
        time.sleep(period)
        self.set_output(0, 1, 0, 1)
        time.sleep(period)
        self.set_output(0, 1, 1, 0)
        time.sleep(period)
        self.set_output(1, 0, 1, 0)
        time.sleep(period)
        self.location -= self.lps
        return

    def auto_up_left(self, period: float) -> None:
        while self.location > 0:
            self.up_left_wards(period)
        return

    def auto_down_right(self, period: float, track_length: float) -> None:
        while self.location < track_length:
            self.down_right_wards(period)
        return

    def down_right_wards(self, period: float) -> None:
        period /= 4
        self.set_output(1, 0, 1, 0)
        time.sleep(period)
        self.set_output(0, 1, 1, 0)
        time.sleep(period)
        self.set_output(0, 1, 0, 1)
        time.sleep(period)
        self.set_output(1, 0, 0, 1)
        time.sleep(period)
        self.location += self.lps
        return

    def clean(self) -> None:
        '''clean the output of the motor to none
        '''
        self.set_output(False, False, False, False)
        return

    def manual_control(self, period: float, steps: int, towards: Literal["left", "up", "right", "down"]) -> None:
        for i in range(steps):
            if towards == ("left" or "up"):
                self.up_left_wards(period)
            elif towards == ("right" or "down"):
                self.down_right_wards(period)

    def reset_location(self):
        self.location = 0
