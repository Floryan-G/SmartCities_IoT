# EX3 — Thermostat MicroPython (Pico W + LCD)

Mini-thermostat : la **consigne** est réglée par potentiomètre (15–35 °C), la **température ambiante** vient d’un **DHT11** (~1 Hz) et s’affiche sur l’écran **Grove JHD1802M1** (contrôleur texte I²C `0x3E`, RGB optionnel).  
LED et buzzer réagissent selon l’écart **Ambient vs Set**.


## Matériel

- Raspberry Pi **Pico W** 
- **Écran LCD**
- **DHT11**
- **Potentiomètre**
- **LED**
- **Buzzer**

> Le driver LCD détecte automatiquement la présence du RGB (`0x62`). S’il n’existe pas, il **l’ignore** (pas d’erreur).


## Arborescence

EX3-Thermostat/
├─ blink.py # programme principal
└─ grove_rgb_lcd.py # driver LCD (texte 0x3E + RGB auto si présent) -> trouver sur internet


## Déploiement rapide

1. **Upload** le projet vers le Pico
2. **Upload** exécuter le fichier


## Comportement

- **LCD**
  - Ligne 1 : `Set: XX.XC` + `ALARM` si ambient > set + 3°C.
  - Ligne 2 : `Ambient: YY.YC` = dernière valeur valide.
- **Règles LED / Buzzer**
  - Si **Ambient > Set + 3 °C** -> **ALARME** : LED **4 Hz**, **buzzer 2 kHz**.
  - Si **Ambient > Set** (sans dépasser +3 °C) -> LED **0,5 Hz**, buzzer **OFF**.
  - Si **Set > Ambient** -> **LED éteinte (OFF)**, buzzer **OFF**.
- **Lecture capteurs** : DHT11 toutes ~**1 s**.
