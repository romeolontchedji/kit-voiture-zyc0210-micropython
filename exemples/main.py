"""
Programme de demonstration : la voiture avance 2 s, recule 2 s, puis
execute la sequence de prise d'objet avec le bras robotise.

A copier sur l'ESP32 sous le nom main.py pour qu'il s'execute
automatiquement au demarrage de la carte (voir README).
"""

import time
from zyc0210 import moveForward, moveBackward, stopMoving, takeObject

moveForward()
time.sleep(2)
stopMoving()
time.sleep_ms(500)

moveBackward()
time.sleep(2)
stopMoving()
time.sleep_ms(500)

takeObject()
