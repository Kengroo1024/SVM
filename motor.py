#!usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import RPi.GPIO as GPIO


class Motor():
    '''用于操作电机的类
    '''

    def __init__(self, pulPlus: int, pulMinus: int, dirPlus: int, dirMinus: int) -> None:
        self.pulPlus = pulPlus
        self.pulMinus = pulMinus
        self.dirPlus = dirPlus
        self.dirMinus = dirMinus

        # GPIO相关设定
        GPIO.setmode(GPIO.BCM)
        for pin in [pulPlus, pulMinus, dirPlus, dirMinus]:
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

    def up_left_wards(self, t: float, period: float) -> None:
        steps = int(t/period)
        period /= 4
        for i in range(steps):
            self.set_output(1, 0, 0, 1)
            time.sleep(period)
            self.set_output(0, 1, 0, 1)
            time.sleep(period)
            self.set_output(0, 1, 1, 0)
            time.sleep(period)
            self.set_output(1, 0, 1, 0)
            time.sleep(period)
        self.reset()
        return

    def down_right_wards(self, t: float, period: float) -> None:
        steps = int(t/period)
        period /= 4
        for i in range(steps):
            self.set_output(1, 0, 1, 0)
            time.sleep(period)
            self.set_output(0, 1, 1, 0)
            time.sleep(period)
            self.set_output(0, 1, 0, 1)
            time.sleep(period)
            self.set_output(1, 0, 0, 1)
            time.sleep(period)
        self.reset()
        return

    def reset(self) -> None:
        '''Reset the output of the motor to none
        '''
        self.set_output(False, False, False, False)
        return
