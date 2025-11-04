# Détection de "battements" avec Raspberry Pi Pico

Projet MicroPython : faire changer la couleur d’une **LED RGB** à chaque **pic sonore** mesuré par un **micro**.

--> Méthode simple : détection de **pics d’amplitude** (sons forts/claquements). Ce n’est pas une détection musicale avancée du tempo.

---

## Matériel

- Raspberry Pi Pico
- micro analogique
- LED RGB

---

## Câblage

Micro analogique --> **A0**
LED RGB --> **D18**

---

## Utilisation

1. Lancer un son (musique avec kick, claquement, ... près du micro).
2. La LED **change de couleur** quand un **pic** dépasse le seuil.

---

## Paramètres à ajuster

- **seuil** (sensibilité)  
  - Trop de déclenchements --> **augmenter** (exemple: entre 30 000 – 50 000)  
  - Pas assez réactif --> **diminuer** (ex. 15 000 – 30 000)
- **Période de changement de couleur** (intervalle en ms)  
  - Plus petite = plus réactif
  - Plus grande = moins de charge CPU

---

## Fonctionnement (résumé)

1. Lecture **constante** de la valeur du micro.
2. Comparaison à un **seuil fixe**.
3. Si dépassé --> **changement aléatoire** de la couleur de la LED RGB.
