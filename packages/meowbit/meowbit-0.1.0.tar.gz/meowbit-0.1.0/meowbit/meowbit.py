import sys, os, platform
import re
from functools import wraps
import serial.tools.list_ports as list_ports
import time
from .SerialCom import serialList, serialCom
from .pyboard import Pyboard, PyboardError


def func_wrap(func):
  @wraps(func)
  def f(*args, **kwargs):
    print(func, args[0].ctx)
    return func(*args, kwargs)
  return f


initCode = '''
import gc,os
gc.enable()
from meowbit import *
from meowbit import Ultrasonic as MeowUltrasonic
'''

HEART = [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0]
HEART_SMALL = [0,0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0]
YES = [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0]
NO = [1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1]
HAPPY = [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0]
SAD = [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1]
CONFUSED = [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1]
ANGRY = [1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,0,1]
ASLEEP = [0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0]
SURPRISED = [0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0]
SILLY = [1,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,1,0,1,0,0,1,1,1]
FABULOUS = [1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,1,0,0,1,1,1,0]
MEH = [1,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]
TSHIRT = [1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0]
ROLLERSKATE = [0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0]
DUCK = [0,1,1,0,0,1,1,1,0,0,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0]
HOUSE = [0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,0,1,0,1,0]
TORTOISE = [0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,0,0,0,0,0]
BUTTERFLY = [1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,0,1,1]
STICKFIGURE = [0,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1]
GHOST = [0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1]
SWORD = [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0]
GIRAFFE = [1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,0]
SKULL = [0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0]
UMBRELLA = [0,1,1,1,0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0]
SNAKE = [1,1,0,0,0,1,1,0,1,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0]
RABBIT = [1,0,1,0,0,1,0,1,0,0,1,1,1,1,0,1,1,0,1,0,1,1,1,1,0]
COW = [1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0]

buzzAPI = ['tone', 'note', 'rest', 'melody', 'stop']
displayAPI = ['scroll', 'show', 'pix', 'clear']
sensorAPI = ['getTemp', 'getLight', 'accX', 'accY', 'accZ', 'gyroX', 'gyroy', 'gyroZ', 'pitch', 'roll', 'gesture', 'btnValue']
screenAPI = ['refresh', 'pixel', 'setColor', 'textSize', 'text', 'textCh', 'showText', 'fill', 'clear', 'pixel', 'line', 'drawLine', 'rect', 
              'drawRect', 'triangle', 'circle', 'drawCircle', 'loadBmp', 'loadgif', 'polygon', 'drawPolygon']

class DummyClass:

  def __init__(self, context):
    self.ctx = context

class MeowBit:

  def __init__(self):
    self.createApi(buzzAPI, 'buzz')
    self.createApi(displayAPI, 'display')
    self.createApi(sensorAPI, 'sensor')
    self.createApi(screenAPI, 'screen')

  def createApi(self, api, namespace):
    setattr(self, namespace, DummyClass(self))
    for n in api:
      f = self.makefunc('display.'+n)
      setattr(getattr(self, namespace), n, f)

  def makefunc(self, callsign):
    def f(*args, **kwargs):
      # print(callsign, args, kwargs)
      tmpArgs=""
      for n in args:
        if type(n) == str:
          tmpArgs+='"%s",' %n
        else:
          tmpArgs+='%s,' %n
      if len(kwargs):
        for key, value in kwargs.items():
          tmpArgs += '%s=%s,' %(key,value)
      code = "%s(%s)" %(callsign, tmpArgs)
      print("exec[", code, "]")
      return self.pyb.eval(code)
    return f

  def commRx(self, msg, dt):
    if msg == None and dt == -1:
      print("Error comm close")
    else:
      print(msg)
      'do port command parse'

  def connect(self, port=None, baud=115200):
    if not port:
      port = serialList()
      if len(port) == 0:
        raise Exception("Cannot find port for board")
      port = port[0]['peripheralId']
    self.comm = serialCom(self.commRx)
    self.comm.connect(port, baud)
    self.pyb = Pyboard(self.comm)
    self.comm.setPybMutex(True)
    self.pyb.enter_raw_repl()
    self.pyb.exec_(initCode)
    time.sleep(0.2)
