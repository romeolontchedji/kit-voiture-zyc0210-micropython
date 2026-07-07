"""
Suivi de personne/objet autonome, a l'aide de lib/zyc0210.py.

    distance < 15 cm          -> recule
    15 cm <= distance < 20 cm -> s'arrete
    distance >= 20 cm         -> avance
"""

from zyc0210 import followMe

followMe()
