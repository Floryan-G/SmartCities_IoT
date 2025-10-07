# Raspberry Pi Pico / MicroPython — TP & Ressources

Ce dépôt regroupe mes notes, codes et supports pour apprendre **MicroPython** sur **Raspberry Pi Pico / Pico W**.

## Description rapide

- **Raspberry Pi Pico / Pico W** : microcontrôleur basé sur **RP2040**, 2 cœurs **ARM Cortex‑M0+** @ 133 MHz, 264 KB de SRAM, USB, GPIO, ADC, PWM. La version **Pico W** ajoute le **Wi‑Fi**.
- **MicroPython** : port du langage Python pour microcontrôleurs. Il permet d’accéder simplement au matériel (GPIO, ADC, PWM, I²C, SPI, UART…).
- **Environnement de travail** : VS Code + extension MicroPico, firmware MicroPython pour Pico/Pico W, sauvegarde des scripts en `main.py`.

### Brochage Pico W (utile pour repérer les GPIO)
![Pinout Pico W](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-2-r4-pinout.svg)
> Source : [Raspberry pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html).

> Astuce : la **LED intégrée** du Pico W est accessible via `machine.Pin("LED")` (selon le firmware). Pour une LED **externe**, choisir une broche GPIO (ex. `GP16`) + résistance 220–330 Ω.

---

## Structure du dépôt

Chaque sous-dossier possède un `README.md` avec les explications, schémas et codes associés :

- [GPIO](GPIO/)   LED simple, bouton‑poussoir, interruption
- [AD-PWM](AD-PWM/)   Lecture ADC (potentiomètre), PWM (LED, musique, servo)
- [LCD](LCD/)   Fonctions de la librairie LCD, affichage ADC
- [LED_neo](LED_neo/)   NeoPixel : guide d’utilisation et démos
- [sensors](sensors/)   Température & humidité, luminosité, PIR
- [network](network/)   Accès réseau avec le Pico W

> Les dossiers non encore réalisés sont des placeholders. Ils seront complétés au fur et à mesure.

---

## Pré‑requis rapides

1. Installer **MicroPython** sur la carte : maintenir **BOOTSEL**, brancher en USB, copier le `.uf2` officiel.   
2. Tester :

```python
from machine import Pin
from time import sleep
led = Pin("LED", Pin.OUT)  # ou Pin(16, Pin.OUT) avec LED externe
while True:
    led.toggle()
    sleep(0.5)
```

