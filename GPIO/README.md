# GPIO — LED + Bouton‑poussoir (+ interruptions)

Ce répertoire contient l’exercice **« Clignotement de LED avec bouton poussoir »** et ses variantes.

## Objectif
Faire clignoter une LED à **différentes vitesses** en fonction du **nombre d’appuis** sur un **bouton poussoir**.

### Matériel
- Raspberry Pi **Pico / Pico W**
- 1× LED + résistance 220–330 Ω (résistance variable intégrée au module)
- 1× bouton poussoir
- Câbles

### Câblage (exemple)
- **LED** : module relié au `GP16`.  
- **Bouton** : module relié au `GP18`.

> Sur Pico W, la **LED interne** peut être pilotée via `Pin("LED")` (`LED_PIN` si vous utilisez une LED externe).

---

## Version 1 — Polling simple (3 vitesses)

- 1er appui : clignote à **0,5 Hz**  (1 s ON/OFF)  
- 2e appui  : clignote à **0,25 Hz** (0,5 s ON/OFF)
- 3e appui  : **LED éteinte**        (stop)

---

## Version 2 — Bonus
 
- 1er appui  : clignote à **0,5 Hz**    (1 s ON/OFF)
- 2ème appui : clignote à **0,25 Hz**  (0,5 s ON/OFF)    --> 0,5 / 2
- 3ème appui : clignote à **0,166 Hz** (0,332 s ON/OFF) --> 0,5 / 3
- 4ème appui : clignote à **0,125 Hz** (0,25 s ON/OFF)  --> 0,5 / 4
- 5ème appui : clignote à **0,1 Hz**   (0,2 s ON/OFF)     --> 0,5 / 5
- 6ème appui : **LED éteinte**         (stop)

---

## Ce que je vérifie
- Détection fiable des appuis (pas de rebond visible)  
- Alternance correcte des modes/vitesses  
- Aucun blocage (la LED continue de clignoter pendant les interactions)
