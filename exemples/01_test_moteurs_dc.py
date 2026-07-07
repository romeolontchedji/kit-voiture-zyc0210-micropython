"""
Test de base des 4 moteurs DC, sans dependance a la librairie lib/zyc0210.py.

Objectif : verifier que le cablage des moteurs sur la carte d'extension
est correct avant d'aller plus loin. Le script fait tourner la voiture
vers la gauche pendant 500 ms puis s'arrete.

Cablage :
    Moteur avant droit   : avancer = GPIO27, reculer = GPIO23
    Moteur arriere droit : avancer = GPIO33, reculer = GPIO32
    Moteur avant gauche  : avancer = GPIO18, reculer = GPIO19
    Moteur arriere gauche: avancer = GPIO26, reculer = GPIO25
"""

from machine import Pin
import time

RightFrontFWD = Pin(27, Pin.OUT)
RightFrontBWD = Pin(23, Pin.OUT)
RightBackFWD = Pin(33, Pin.OUT)
RightBackBWD = Pin(32, Pin.OUT)

LeftFrontFWD = Pin(18, Pin.OUT)
LeftFrontBWD = Pin(19, Pin.OUT)
LeftBackFWD = Pin(26, Pin.OUT)
LeftBackBWD = Pin(25, Pin.OUT)


def moveForward():
    RightFrontFWD.value(1)
    RightFrontBWD.value(0)
    RightBackFWD.value(1)
    RightBackBWD.value(0)

    LeftFrontFWD.value(1)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(1)
    LeftBackBWD.value(0)


def moveBackward():
    RightFrontFWD.value(0)
    RightFrontBWD.value(1)
    RightBackFWD.value(0)
    RightBackBWD.value(1)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(1)
    LeftBackFWD.value(0)
    LeftBackBWD.value(1)


def rotateLeft():
    RightFrontFWD.value(1)
    RightFrontBWD.value(0)
    RightBackFWD.value(1)
    RightBackBWD.value(0)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(1)
    LeftBackFWD.value(0)
    LeftBackBWD.value(1)


def rotateRight():
    RightFrontFWD.value(0)
    RightFrontBWD.value(1)
    RightBackFWD.value(0)
    RightBackBWD.value(1)

    LeftFrontFWD.value(1)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(1)
    LeftBackBWD.value(0)


def stopMoving():
    RightFrontFWD.value(0)
    RightFrontBWD.value(0)
    RightBackFWD.value(0)
    RightBackBWD.value(0)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(0)
    LeftBackBWD.value(0)


rotateLeft()
time.sleep_ms(500)
stopMoving()
