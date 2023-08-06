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

# melody
CORRECT = "c6:1 f6:2"
NOTICE = "d5:1 b4:1"
ERROR = "a3:2 r a3:2"
DADA = "r4:2 g g g eb:8 r:2 f f f d:8 "
ENTERTAINER = "d4:1 d# e c5:2 e4:1 c5:2 e4:1 c5:3 c:1 d d# e c d e:2 b4:1 d5:2 c:4 "
PRELUDE = "c4:1 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e c4 d g d5 f g4 d5 f c4 d g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f c4 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e "
ODE = "e4 e f g g f e d c c d e e:6 d:2 d:8 e:4 e f g g f e d c c d e d:6 c:2 c:8 "
NYAN = "f#5:2 g# c#:1 d#:2 b4:1 d5:1 c# b4:2 b c#5 d d:1 c# b4:1 c#5:1 d# f# g# d# f# c# d b4 c#5 b4 d#5:2 f# g#:1 d# f# c# d# b4 d5 d# d c# b4 c#5 d:2 b4:1 c#5 d# f# c# d c# b4 c#5:2 b4 c#5 b4 f#:1 g# b:2 f#:1 g# b c#5 d# b4 e5 d# e f# b4:2 b f#:1 g# b f# e5 d# c# b4 f# d# e f# b:2 f#:1 g# b:2 f#:1 g# b b c#5 d# b4 f# g# f# b:2 b:1 a# b f# g# b e5 d# e f# b4:2 c#5 "
RING = "c4:1 d e:2 g d:1 e f:2 a e:1 f g:2 b c5:4 "
FUNK = "c2:2 c d# c:1 f:2 c:1 f:2 f# g c c g c:1 f#:2 c:1 f#:2 f d# "
BLUES = "c2:2 e g a a# a g e c2:2 e g a a# a g e f a c3 d d# d c a2 c2:2 e g a a# a g e g b d3 f f2 a c3 d# c2:2 e g e g f e d "
BIRTHDAY = "c4:3 c:1 d:4 c:4 f e:8 c:3 c:1 d:4 c:4 g f:8 c:3 c:1 c5:4 a4 f e d a#:3 a#:1 a:4 f g f:8 "
WEDDING = "c4:4 f:3 f:1 f:8 c:4 g:3 e:1 f:8 c:4 f:3 a:1 c5:4 a4:3 f:1 f:4 e:3 f:1 g:8 "
FUNERAL = "c3:4 c:3 c:1 c:4 d#:3 d:1 d:3 c:1 c:3 b2:1 c3:4 "
PUNCHLINE = "c4:3 g3:1 f# g g#:3 g r b c4 "
BADDY = "c3:3 r d:2 d# r c r f#:8 "
CHASE = "a4:1 b c5 b4 a:2 r a:1 b c5 b4 a:2 r a:2 e5 d# e f e d# e b4:1 c5 d c b4:2 r b:1 c5 d c b4:2 r b:2 e5 d# e f e d# e "
BA_DING = "b5:1 e6:3 "
WAWA = "e3:3 r:1 d#:3 r:1 d:4 r:1 c#:8 "
JUMP_UP = "c5:1 d e f g "
JUMP_DOWN = "g5:1 f e d c "
POWER_UP = "g4:1 c5 e g:2 e:1 g:3 "
POWER_DOWN = "g5:1 d# c g4:2 b:1 c5:3 "

buzzAPI = ['tone', 'note', 'rest', 'melody', 'stop']
displayAPI = ['scroll', 'show', 'pix', 'clear']
sensorAPI = ['getTemp', 'getLight', 'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ', 'pitch', 'roll', 'gesture', 'btnValue']
screenAPI = ['refresh', 'pixel', 'setColor', 'textSize', 'text', 'textCh', 'showText', 'fill', 'clear', 'pixel', 'line', 'drawLine', 'rect', 
              'drawRect', 'triangle', 'circle', 'drawCircle', 'loadBmp', 'loadgif', 'polygon', 'drawPolygon', 'sync']

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class DummyClass:

  def __init__(self, context):
    self.ctx = context

class MeowBit:

  def __init__(self):
    self.funcPre = {"screen.textCh": self.textChPre}
    self.createApi(buzzAPI, 'buzzer')
    self.createApi(displayAPI, 'display')
    self.createApi(sensorAPI, 'sensor')
    self.createApi(screenAPI, 'screen')
    self.fontfd = open(os.path.join(os.path.dirname(__file__), 'font_12x16.bin'), 'rb')


  def __del__(self):
    self.fontfd.close()

  def textChPre(self, args, kwargs):
    fontDict = {}
    for n in range(len(args[0])):
      unicode = ord(args[0][n])
      self.fontfd.seek(unicode*24)
      fontDict[str(unicode)] = list(bytes(self.fontfd.read(24)))

    kwargs['font'] = fontDict
    return (args, kwargs)

  def createApi(self, api, namespace):
    setattr(self, namespace, DummyClass(self))
    for n in api:
      f = self.makefunc(namespace+'.'+n)
      setattr(getattr(self, namespace), n, f)

  def makefunc(self, callsign):
    def f(*args, **kwargs):
      # print(callsign, args, kwargs)
      tmpArgs=""
      if callsign in self.funcPre:
        (args, kwargs) = self.funcPre[callsign](args, kwargs)
      for n in args:
        if type(n) == str:
          tmpArgs+='"%s",' %n
        else:
          tmpArgs+=str(n)+','
      if len(kwargs):
        for key, value in kwargs.items():
          tmpArgs += '%s=%s,' %(key,value)
      code = "%s(%s)" %(callsign, tmpArgs)
      # print("exec[", code, "]")
      ret = self.pyb.eval(code)
      try:
        ret = ret.decode()
        if ret.isnumeric():
          return int(ret)
        elif isfloat(ret):
          return float(ret)
        elif ret == 'True' or ret == 'true' or ret == '1':
          return True
        elif ret == 'False' or ret == 'false' or ret == '0':
          return False
        else:
          return ret
      except:
        return ret
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
