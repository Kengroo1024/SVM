#!usr/bin/env python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
from model import *
from motor import *
from formatting import *

'''
程序运行入口
'''


def main():
    pass


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
        print("GPIO已复位")
