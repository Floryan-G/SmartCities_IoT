# Utilise des endpoints texte (HTTP) adaptés à MicroPython:
#   - ip-api (fuseau):       http://ip-api.com/line?fields=timezone
#   - worldtimeapi (offset): http://worldtimeapi.org/api/ip.txt
#                             ou /api/timezone/<TZ>.txt
#
# On privilégie raw_offset + dst_offset (en secondes) pour gérer été/hiver.

import time
import network
import ntptime
import urequests

def connecter_wifi(ssid, mot_de_passe):
    # Active l'interface STA, se connecte au Wi-Fi et affiche la config IP
    # Bloque jusqu'à connexion
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, mot_de_passe)
        while not wlan.isconnected():
            time.sleep(0.2)
    print("Wi-Fi OK :", wlan.ifconfig())

def telecharger_texte(url):
    r = urequests.get(url)
    try:
        texte = r.text
    finally:
        try:
            r.close()
        except:
            pass
    return texte

def detecter_fuseau():
    # Détectecte le fuseau automatiquement via ip-api (réponse en 1 ligne ou None si pas dispo)

    try:
        texte = telecharger_texte("http://ip-api.com/line?fields=timezone")
        tz = texte.strip()
        print("Fuseau détecté :", tz)
        return tz if tz and tz != "fail" else None
    except Exception as e:
        print("Impossible de détecter le fuseau :", e)
        return None

def _parse_utc_offset_str(utc_offset_str):
    # Convertit une chaîne du type '+01:00' ou '-05:30' en secondes (int)
    
    signe = 1 if utc_offset_str[0] == "+" else -1
    heures = int(utc_offset_str[1:3])
    minutes = int(utc_offset_str[4:6])
    return signe * (heures * 3600 + minutes * 60)

def offset_depuis_internet(fuseau_hint=None):
    #Renvoie l'offset total UTC->local en SECONDES, obtenu via WorldTimeAPI.
    # Priorité:
    #   1) /api/ip.txt (auto par IP)
    #   2) /api/timezone/<fuseau>.txt si on a un fuseau
    #   3) /api/timezone/Europe/Brussels.txt en secours
    # On privilégie raw_offset + dst_offset (déjà en secondes)

    urls = ["http://worldtimeapi.org/api/ip.txt"]
    if fuseau_hint:
        urls.append("http://worldtimeapi.org/api/timezone/" + fuseau_hint + ".txt")
    urls.append("http://worldtimeapi.org/api/timezone/Europe/Brussels.txt")

    for url in urls:
        try:
            texte = telecharger_texte(url)

            raw_off = None
            dst_off = 0
            utc_off_str = None

            for ligne in texte.splitlines():
                l = ligne.strip()
                if l.startswith("raw_offset:"):
                    raw_off = int(l.split(":", 1)[1].strip())
                elif l.startswith("dst_offset:"):
                    dst_off = int(l.split(":", 1)[1].strip())
                elif l.startswith("utc_offset:"):
                    utc_off_str = l.split(":", 1)[1].strip()

            if raw_off is not None:
                total = raw_off + (dst_off or 0)
                print("Décalage (raw+dst) :", total, "s  via", url)
                return total
            if utc_off_str:
                total = _parse_utc_offset_str(utc_off_str)
                print("Décalage (utc_offset str) :", utc_off_str, "=>", total, "s  via", url)
                return total
        except Exception as e:
            print("Échec sur", url, "->", e)

    # Secours minimal : +3600 (Belgique en hiver)
    print("Fallback offset : +3600 s (Belgique)")
    return 3600

def regler_heure_ntp(reessaies=3):
    # Lance ntptime.settime() avec quelques réessais
    # Renvoie True si OK, False sinon

    for i in range(reessaies):
        try:
            ntptime.settime()
            return True
        except Exception as e:
            print("NTP échec", i+1, "/", reessaies, ":", e)
            time.sleep(1 + i)
    return False

def heure_locale(decalage_s):
    # Met à l’heure en UTC via NTP puis applique l’offset pour renvoyer un struct_time local
    # Lève OSError si NTP indisponible (à rattraper coté main)

    if not regler_heure_ntp():
        raise OSError("NTP indisponible")
    t = time.time() + decalage_s
    return time.localtime(t)
