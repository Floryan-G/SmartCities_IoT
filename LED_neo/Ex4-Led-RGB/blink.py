from machine import ADC, Pin
import urandom
import neopixel
from time import ticks_ms, ticks_diff

micro = ADC(26)                           # A0
led_rgb = neopixel.NeoPixel(Pin(18), 1)   # D18

def definir_couleur(r, v, b):
    led_rgb[0] = (r, v, b)
    led_rgb.write()

def couleur_aleatoire():
    r = urandom.getrandbits(8)
    v = urandom.getrandbits(8)
    b = urandom.getrandbits(8)
    
    if r < 40 and v < 40 and b < 40:    # éviter le noir complet
        r = 255
    definir_couleur(r, v, b)


seuil = 20000         # seuil pour éviter de lire les bruits

dernier_echant_ms = ticks_ms()
dernier_battement_ms = ticks_ms()

pic_observe = 0
valeur = 0

definir_couleur(0, 0, 0)

while True:
    maintenant = ticks_ms()

    valeur = micro.read_u16()       # Lire le micro

    if ticks_diff(maintenant, dernier_echant_ms) >= 100:    # lecture des données toutes les 200 ms
        dernier_echant_ms = maintenant

        if valeur > seuil:      # verifications des valeurs + changement couleur led
            couleur_aleatoire()
            print(valeur)
