"""
Suivi de ligne noire en boucle, a l'aide de lib/zyc0210.py.

Pensez a calibrer BlackLine dans lib/zyc0210.py avec
exemples/04_test_capteurs_ligne.py avant d'utiliser ce script.
"""

from zyc0210 import lineTracking
import time

while True:
    lineTracking()
    time.sleep_ms(10)
