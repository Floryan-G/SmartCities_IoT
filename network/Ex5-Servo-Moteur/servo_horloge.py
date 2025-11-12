from machine import Pin, PWM

# Ajustement des bornes du servo (0 à 180 degrés)
DUTY_MIN = 2100   # 0°
DUTY_MAX = 7700   # 180°

class ServoHorloge:
    # Conversion linéaire angle -> duty_u16 entre DUTY_MIN et DUTY_MAX

    def __init__(self, broche):
        self.pwm = PWM(Pin(broche))
        self.pwm.freq(50)

    def _angle_vers_duty(self, angle):
        # Sécurité : on borne l'angle
        if angle < 0:
            angle = 0
        if angle > 180:
            angle = 180

        ratio = angle / 180.0
        return int(DUTY_MIN + (DUTY_MAX - DUTY_MIN) * ratio)

    def positionner(self, angle):
        # Envoie l'angle demandé au servo (0..180°)

        self.pwm.duty_u16(self._angle_vers_duty(angle))
