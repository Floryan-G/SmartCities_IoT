# Projet : Mélodie avec Buzzer et Potentiomètre

Ce projet consiste à générer une mélodie en utilisant un buzzer et à contrôler le volume à l'aide d'un potentiomètre. 

## Matériel utilisé

- **Raspberry Pi Pico W**
- **Buzzer passif** (connecté à la broche GP28)
- **Potentiomètre** (connecté à la broche GP27)

## Fonctionnalités

- **Volume dynamique** : Le volume du buzzer est contrôlé par le potentiomètre. Le son est coupé si la valeur est trop faible (résistance interne) ou trop élevée (saturation).
- **Utilisation de boucle rapide** : Le code s'exécute dans une boucle infinie mais à l'intérieur se cache des boucles qui tournent très vite (10 ms et 500 ms) pour éviter de bloquer le thread.