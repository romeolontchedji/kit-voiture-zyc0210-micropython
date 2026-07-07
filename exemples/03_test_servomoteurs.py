"""
Test des 3 servomoteurs du bras : place chacun a un angle de reference.

Necessite lib/servo.py sur la carte (voir README, section installation).

Cablage : pince = GPIO22, bras = GPIO21, base = GPIO2
"""

from servo import Servo
import time

ClampServo = Servo(22)      # servomoteur de la pince
ArmServo = Servo(21)        # servomoteur du bras
TurnableServo = Servo(2)    # servomoteur de la base

ClampServo.write_angle(48)     # pince
time.sleep_ms(20)
TurnableServo.write_angle(60)  # base
time.sleep_ms(20)
ArmServo.write_angle(45)       # bras
time.sleep_ms(20)
