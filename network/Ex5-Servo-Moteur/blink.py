import time
import internet
from servo_horloge import ServoHorloge

SSID = "iPhone de Flo"
MOT_DE_PASSE = "987654321"
BROCHE_SERVO = 16

PERIODE_MAJ_MS = 30_000   # 30 secondes

def heure_vers_angle(heure, minute):  #calcul de l'angle
    h12 = heure % 12
    angle = h12 * 15
    angle += (minute / 60.0) * 15
    return angle

def angle_inverse(angle):           # inversion pour pas que 00h00 soit en bas et 11h59 en haut
    return 180 - (angle % 180)

def affichage(decalage_s, servo):
    try:
        date_heure = internet.heure_locale(decalage_s)  # struct_time local
        heure = date_heure[3]
        minute = date_heure[4]

        angle = heure_vers_angle(heure, minute)         # logique conservée
        angle_envoye = angle_inverse(angle)             # inversion à l’envoi

        print("Heure locale %02d:%02d | angle=%.2f° -> envoyé=%.2f°"
                % (heure, minute, angle, angle_envoye))

        servo.positionner(angle_envoye)
    except OSError as e:
        # NTP indisponible temporairement : on réessaiera au prochain tick
        print("Erreur temps :", e)

def main():
    # 1) Connexion Wi-Fi
    internet.connecter_wifi(SSID, MOT_DE_PASSE)

    # 2) Fuseau + offset
    fuseau = internet.detecter_fuseau()
    decalage_s = internet.offset_depuis_internet(fuseau)

    # 3) Servo
    servo = ServoHorloge(BROCHE_SERVO)

    # 4) Scheduler non bloquant
    dernier_tick = time.ticks_ms()   # instant de référence

    affichage(decalage_s, servo)

    while True:
        # Tick courant
        maintenant = time.ticks_ms()

        # Si 30 s (ou plus) se sont écoulées, on exécute la mise à jour
        if time.ticks_diff(maintenant, dernier_tick) >= PERIODE_MAJ_MS:
            affichage(decalage_s, servo)

            # Recalage du prochain déclenchement sans dérive
            # (on ajoute 30 s à l'ancien tick plutôt que de repartir de 'maintenant')
            dernier_tick = time.ticks_add(dernier_tick, PERIODE_MAJ_MS)

if __name__ == "__main__":
    main()
