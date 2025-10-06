import time
import machine

led = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
nb = 0
etat = 0
etat_precedant = 0
temps_base = 0.5

def clignotte (temps):
    led.toggle()
    time.sleep(temps)
    led.toggle()
    time.sleep(temps)

while True:
    etat = button.value()

    if etat == 1 and etat_precedant == 0:
        nb += 1
    
    if nb == 1:
        clignotte(temps_base)
    elif nb == 2:
        clignotte(temps_base/2)
    else:
        nb = 0
        led.value(0)

    etat_precedant = etat