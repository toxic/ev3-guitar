#!/usr/bin/env python3

from ev3dev2.sound import Sound
from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.button import Button
import math
import sys
import random

print("Welcome to EV3 Guitar")

sound = Sound()
ir = InfraredSensor()
ts = TouchSensor()
servo = MediumMotor()
button = Button()

# params
multiply = 1
step = [5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70]
sound.set_volume(5)

def volumeUp(state):
  current = int(sound.get_volume())
  if current < 100:
    sound.set_volume(current + 1)
    print("Volume: " + str(current + 1))

def volumeDown(state):
  current = int(sound.get_volume())
  if current > 0:
    sound.set_volume(current - 1)
    print("Volume: " + str(current - 1))                                                  

def backButton(state):
  print("Bye!!")
  sys.exit()

def multiplyUp(state):
  multiply = multiply + 1

def multiplyDown(state):
  multiply = multiply - 1

button.on_up = volumeUp
button.on_down = volumeDown
button.on_left = multiplyUp
button.on_right = multiplyDown
button.on_backspace = backButton

# app run
while True:
  button.process()
  distance = int(math.fabs(ir.value()))
  position = int(math.fabs(servo.position))

  for x in step:
    if distance <= x:
      hertz = int(x * 15)
      print("Hertz - " + str(hertz))
      break

  for x in step:
    if position <= x:
      duration = int(x * 5 * multiply)
      print("Duration - " + str(duration))
      break

  if ts.is_pressed:
    if delay == 200:
      print("Delay Off")
    delay = 0
  else:
    if delay == 0:
      print("Delay On")
    delay = 200

  # onOff = 'on' if delay == 200 else 'off'
  # print("Hz: " + str(hertz) + " Lenght: " + str(duration) + " Delay: " + str(onOff))

  sound.tone([
    (hertz, duration, delay)
  ])
