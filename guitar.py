#!/usr/bin/env python3

import math
import sys

from ev3dev2.button import Button
from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor
from ev3dev2.sound import Sound

class Guitar:
  def __init__(self):
    print("Welcome to EV3 Guitar")

    self.sound = Sound()

    # mount function
    self.multiply = 1
    self.pause = False
    self.volume = 10

    # set initial volume
    self.setVolume(50)

  def getVolume(self):
    return int(self.sound.get_volume('Beep'))

  def setVolume(self, volume):
    self.sound.set_volume(int(volume), 'Beep')

  def volumeUp(self, state):
    if state:
      if self.volume < 100:
        self.sound.set_volume(self.volume + 1)

  def volumeDown(self, state):
    if state:
      if self.volume > 0:
        self.sound.set_volume(self.volume - 1)                                             

  def backButton(self, state):
    print("Bye!!")
    sys.exit()

  def multiplyUp(self, state):
    self.multiply = self.multiply + 1

  def multiplyDown(self, state):
    if self.multiply > 1:
      self.multiply = self.multiply - 1

  def togglePause(self, state):
    if state and self.pause:
      self.pause = False
    else:
      self.pause = True

  # app run
  def play(self):
    delay = 0
    step = [5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70]

    button = Button()
    button.on_up = self.volumeUp
    button.on_down = self.volumeDown
    button.on_left = self.multiplyUp
    button.on_right = self.multiplyDown
    button.on_enter = self.togglePause
    button.on_backspace = self.backButton

    ir = InfraredSensor()
    ts = TouchSensor()
    servo = MediumMotor()

    while True:
      self.volume = self.getVolume()
      button.process()
      
      if self.pause == True:
        continue

      distance = int(math.fabs(ir.value()))
      position = int(math.fabs(servo.position))

      for x in step:
        if distance <= x:
          hertz = int(x * 15)
          # print("Hertz - " + str(hertz))
          break

      for x in step:
        if position <= x:
          duration = int(x * 5 * self.multiply)
          # print("Duration - " + str(duration))
          break

      if ts.is_pressed:
        if delay == 200:
          delay = 0
      else:
        if delay == 0:
          delay = 200
      
      # play sound
      self.sound.tone([
        (hertz, duration, delay)
      ])


Guitar().play()