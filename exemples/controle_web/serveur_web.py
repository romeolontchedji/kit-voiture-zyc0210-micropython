"""
Controle de la voiture a distance depuis un navigateur web.

L'ESP32 cree son propre point d'acces Wi-Fi et heberge une page web
(index.html) avec des boutons Avancer / Reculer / Gauche / Droite / Stop.
Chaque bouton declenche une requete HTTP recue et traitee ici.

A copier sur l'ESP32 en meme temps que index.html (meme dossier), puis
executer ce script (ou le renommer main.py pour un lancement automatique).

Une fois lance, connectez un telephone ou un PC au reseau Wi-Fi
"voiture-robot" (mot de passe "voiture1234") puis ouvrez un navigateur a
l'adresse http://192.168.4.1
"""

import network
import socket
from machine import Pin

# ================== MOTEURS DC ==================
RightFrontFWD = Pin(27, Pin.OUT)
RightFrontBWD = Pin(23, Pin.OUT)
RightBackFWD = Pin(33, Pin.OUT)
RightBackBWD = Pin(32, Pin.OUT)

LeftFrontFWD = Pin(18, Pin.OUT)
LeftFrontBWD = Pin(19, Pin.OUT)
LeftBackFWD = Pin(26, Pin.OUT)
LeftBackBWD = Pin(25, Pin.OUT)


def stop():
    for p in (
        RightFrontFWD, RightFrontBWD,
        RightBackFWD, RightBackBWD,
        LeftFrontFWD, LeftFrontBWD,
        LeftBackFWD, LeftBackBWD,
    ):
        p.value(0)


def forward():
    stop()
    RightFrontFWD.value(1)
    RightBackFWD.value(1)
    LeftFrontFWD.value(1)
    LeftBackFWD.value(1)


def backward():
    stop()
    RightFrontBWD.value(1)
    RightBackBWD.value(1)
    LeftFrontBWD.value(1)
    LeftBackBWD.value(1)


def left():
    stop()
    RightFrontFWD.value(1)
    RightBackFWD.value(1)
    LeftFrontBWD.value(1)
    LeftBackBWD.value(1)


def right():
    stop()
    RightFrontBWD.value(1)
    RightBackBWD.value(1)
    LeftFrontFWD.value(1)
    LeftBackFWD.value(1)


# ================== POINT D'ACCES WIFI ==================
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="voiture-robot", password="voiture1234")

print("Point d'acces actif :", ap.ifconfig())

# ================== SERVEUR WEB ==================
ROUTES = {
    "GET /avancer": forward,
    "GET /reculer": backward,
    "GET /gauche": left,
    "GET /droite": right,
    "GET /stop": stop,
}


def load_html():
    with open("index.html", "r") as f:
        return f.read()


PAGE = load_html()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 80))
s.listen(1)

print("Serveur HTTP demarre sur le port 80")

while True:
    conn, addr = s.accept()
    try:
        request = conn.recv(1024).decode()
        request_line = request.split("\r\n", 1)[0]

        action = None
        for route, handler in ROUTES.items():
            if request_line.startswith(route):
                action = handler
                break

        if action is not None:
            action()
            body = "OK"
        else:
            body = PAGE

        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send("Content-Type: text/html\r\n")
        conn.send("Connection: close\r\n\r\n")
        conn.sendall(body)
    finally:
        conn.close()
