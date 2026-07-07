"""
Librairie pour le kit de voiture robotique ZYC0210 (ESP32 + MicroPython).

Regroupe :
    - le pilotage des 4 moteurs DC (avancer, reculer, tourner, arreter) ;
    - la lecture du capteur ultrason HC-SR04 ;
    - le pilotage des 3 servomoteurs du bras (pince, bras, base) et la
      sequence de prise d'objet ;
    - des comportements autonomes prets a l'emploi : evitement d'obstacles,
      suivi de personne, suivi de ligne.

Cablage attendu (voir le README du depot pour le detail) :
    Moteurs DC   : GPIO27/23 (avant droit), GPIO33/32 (arriere droit),
                   GPIO18/19 (avant gauche), GPIO26/25 (arriere gauche)
    Ultrason     : trigger GPIO13, echo GPIO12
    Suivi ligne  : gauche GPIO34, centre GPIO35, droit GPIO14
    Servomoteurs : pince GPIO22, bras GPIO21, base GPIO2
"""

from machine import Pin, ADC
from hcsr04 import HCSR04
from servo import Servo
import time

## Moteurs DC
RightFrontFWD = Pin(27, Pin.OUT)  # moteur avant droit sens avancer
RightFrontBWD = Pin(23, Pin.OUT)  # moteur avant droit sens reculer
RightBackFWD = Pin(33, Pin.OUT)   # moteur arriere droit sens avancer
RightBackBWD = Pin(32, Pin.OUT)   # moteur arriere droit sens reculer

LeftFrontFWD = Pin(18, Pin.OUT)   # moteur avant gauche sens avancer
LeftFrontBWD = Pin(19, Pin.OUT)   # moteur avant gauche sens reculer
LeftBackFWD = Pin(26, Pin.OUT)    # moteur arriere gauche sens avancer
LeftBackBWD = Pin(25, Pin.OUT)    # moteur arriere gauche sens reculer

## Capteur ultrason
ultrason = HCSR04(trigger_pin=13, echo_pin=12)

## Capteurs infrarouges du module suiveur de ligne
LeftSensor = ADC(Pin(34))
CenterSensor = ADC(Pin(35))
RightSensor = ADC(Pin(14))

LeftSensor.atten(ADC.ATTN_11DB)
CenterSensor.atten(ADC.ATTN_11DB)
RightSensor.atten(ADC.ATTN_11DB)

# Seuil de detection de la ligne noire pour le module infrarouge.
# A recalibrer selon la couleur du sol et l'eclairage ambiant
# (afficher LeftSensor.read()/CenterSensor.read()/RightSensor.read() sur
# la ligne et en dehors pour trouver la bonne valeur).
BlackLine = 600

## Servomoteurs du bras
ClampServo = Servo(22)      # servo moteur de la pince
ArmServo = Servo(21)        # servo moteur du bras
TurnableServo = Servo(2)    # servo moteur de la base

# Les angles utilises ci-dessous (initServo, takeObject) correspondent au
# montage d'origine et peuvent ne pas convenir a votre assemblage. Comme
# pour BlackLine, chacun peut faire son propre etalonnage a l'aide de
# exemples/03_test_servomoteurs.py puis reporter les valeurs trouvees ici.


## ----------------------- Bras et pince -----------------------

def initServo():
    """Replace le bras et la pince dans leur position de repos."""
    ClampServo.write_angle(48)
    time.sleep_ms(20)
    TurnableServo.write_angle(60)
    time.sleep_ms(20)
    ArmServo.write_angle(45)
    time.sleep_ms(20)


def takeObject():
    """Sequence complete : ouvrir la pince, descendre, saisir, remonter."""
    initServo()
    for i in range(48, 0, -1):
        ClampServo.write_angle(i)
        time.sleep_ms(15)
    time.sleep_ms(500)
    for i in range(45, 160):
        ArmServo.write_angle(i)
        time.sleep_ms(15)
    time.sleep_ms(500)
    for i in range(0, 36):
        ClampServo.write_angle(i)
        time.sleep_ms(15)
    time.sleep_ms(500)
    for i in range(160, 45, -1):
        ArmServo.write_angle(i)
        time.sleep_ms(15)
    time.sleep_ms(500)


## ----------------------- Capteur ultrason -----------------------

def getDistance():
    """Distance mesuree par le capteur HC-SR04, en millimetres."""
    return ultrason.distance_mm()


## ----------------------- Deplacement -----------------------

def stopMoving():
    RightFrontFWD.value(0)
    RightFrontBWD.value(0)
    RightBackFWD.value(0)
    RightBackBWD.value(0)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(0)
    LeftBackBWD.value(0)


def moveForward():
    stopMoving()
    RightFrontFWD.value(1)
    RightFrontBWD.value(0)
    RightBackFWD.value(1)
    RightBackBWD.value(0)

    LeftFrontFWD.value(1)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(1)
    LeftBackBWD.value(0)


def moveBackward():
    stopMoving()
    RightFrontFWD.value(0)
    RightFrontBWD.value(1)
    RightBackFWD.value(0)
    RightBackBWD.value(1)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(1)
    LeftBackFWD.value(0)
    LeftBackBWD.value(1)


def rotateLeft():
    stopMoving()
    RightFrontFWD.value(1)
    RightFrontBWD.value(0)
    RightBackFWD.value(1)
    RightBackBWD.value(0)

    LeftFrontFWD.value(0)
    LeftFrontBWD.value(1)
    LeftBackFWD.value(0)
    LeftBackBWD.value(1)


def rotateRight():
    stopMoving()
    RightFrontFWD.value(0)
    RightFrontBWD.value(1)
    RightBackFWD.value(0)
    RightBackBWD.value(1)

    LeftFrontFWD.value(1)
    LeftFrontBWD.value(0)
    LeftBackFWD.value(1)
    LeftBackBWD.value(0)


## ----------------------- Comportements autonomes -----------------------

def obstacleAvoidance():
    """Avance tant que la voie est libre, tourne a gauche des qu'un
    obstacle est detecte a moins de 30 cm."""
    while True:
        distance = getDistance()
        if distance < 300:
            stopMoving()
            time.sleep_ms(30)
            rotateLeft()
            time.sleep_ms(500)
            stopMoving()
        else:
            moveForward()
            time.sleep_ms(50)


def followMe():
    """Suit un objet/une personne place(e) devant le capteur ultrason.

        distance < 150         ==> reculer
        150 <= distance < 200  ==> stop
        distance >= 200        ==> avancer
    """
    while True:
        distance = getDistance()

        if distance <= 0:
            stopMoving()
        elif distance < 150:
            moveBackward()
        elif distance <= 200:
            stopMoving()
        else:
            moveForward()
        time.sleep_ms(120)


def lineTracking():
    """Suit une ligne noire grace aux 3 capteurs infrarouges.

    A appeler en boucle (voir exemples/test_suivi_ligne.py).
    """
    LeftValue = LeftSensor.read()
    CenterValue = CenterSensor.read()
    RightValue = RightSensor.read()

    if (LeftValue < BlackLine and
            CenterValue >= BlackLine and
            RightValue < BlackLine):
        moveForward()

    elif (LeftValue >= BlackLine and
            LeftValue > RightValue):
        rotateLeft()

    elif (RightValue >= BlackLine and
            RightValue > LeftValue):
        rotateRight()

    elif (LeftValue >= BlackLine and
            CenterValue >= BlackLine and
            RightValue >= BlackLine):
        stopMoving()

    elif (LeftValue < BlackLine and
            CenterValue < BlackLine and
            RightValue < BlackLine):
        stopMoving()
