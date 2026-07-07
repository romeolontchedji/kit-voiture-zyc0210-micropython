"""
Test des 3 capteurs infrarouges du module suiveur de ligne : affiche en
continu les valeurs analogiques lues sur chaque capteur.

Utile pour calibrer le seuil `BlackLine` de lib/zyc0210.py : notez les
valeurs obtenues au-dessus du sol clair, puis au-dessus de la ligne noire.

Cablage : gauche = GPIO34, centre = GPIO35, droit = GPIO14
"""

from machine import Pin, ADC
import time

LeftSensor = ADC(Pin(34))
CenterSensor = ADC(Pin(35))
RightSensor = ADC(Pin(14))

LeftSensor.atten(ADC.ATTN_11DB)
CenterSensor.atten(ADC.ATTN_11DB)
RightSensor.atten(ADC.ATTN_11DB)

while True:
    print(f"Gauche : {LeftSensor.read()}")
    print(f"Centre : {CenterSensor.read()}")
    print(f"Droite : {RightSensor.read()}")
    print("---")
    time.sleep_ms(1000)
