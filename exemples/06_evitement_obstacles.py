"""
Evitement d'obstacles autonome, a l'aide de lib/zyc0210.py.

La voiture avance tant que la voie est libre et tourne a gauche des
qu'un obstacle est detecte a moins de 30 cm par le capteur ultrason.
"""

from zyc0210 import obstacleAvoidance

obstacleAvoidance()
