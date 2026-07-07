"""
Test du capteur ultrason HC-SR04 : affiche en continu la distance mesuree.

Necessite lib/hcsr04.py sur la carte (voir README, section installation).

Cablage : trigger = GPIO13, echo = GPIO12
"""

from hcsr04 import HCSR04
import time

ultrason = HCSR04(trigger_pin=13, echo_pin=12)

while True:
    distance = ultrason.distance_mm()
    print(distance, "mm")
    time.sleep_ms(500)
