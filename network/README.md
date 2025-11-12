# Horloge NTP + Servo – Raspberry Pi Pico W

Affiche l’heure locale en positionnant un **servo** (0–180°) grâce à une **synchro NTP**, une **détection automatique du fuseau** et un **offset** récupéré sur internet. Boucle **non bloquante** et **inversion mécanique** gérée **sans toucher à la logique d’angle**.

## Fonctionnalités
- Connexion Wi-Fi (SSID/Mot de passe configurables).
- Détection automatique du fuseau (`ip-api.com`).
- Offset UTC total (heure d’été/hiver incluse) via WorldTimeAPI (`raw_offset + dst_offset`).
- Mise à l’heure par NTP avec **réessais**.
- Calcul d’angle : **12h → 0°**, **6h → 90°**, minutes proportionnelles (logique conservée).
- **Inversion** de l’angle juste **avant** l’envoi au servo.
- **Scheduler non bloquant** toutes les 30 s (pas de `sleep` bloquant).

## Configuration
Dans blink.py :
- SSID = "WIFI"
- MOT_DE_PASSE = "MDP"
- DUTY_MIN = 2100 (à tester sur le moteur avec angle 0 et 180 degrés)
- DUTY_MAX = 7700 (à tester sur le moteur avec angle 0 et 180 degrés)

## Déploiement
- exporter le dossier sur le Raspberry Pi Pico W
- Exécuté le fichier courant