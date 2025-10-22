from machine import Pin, PWM, ADC, I2C
from time import ticks_ms, ticks_diff
import dht
from grove_rgb_lcd import GroveRGBLCD # Driver trouver sur internet


PIN_POT  = 26  # A0 -> GP26
PIN_LED  = 18  # D18 -> GP18
PIN_BUZZ = 20  # D20 -> GP20 (PWM)
PIN_DHT  = 16  # D16 -> GP16


CONS_MIN, CONS_MAX = 15.0, 35.0
DELTA_AL = 3.0
F_LED_NORM = 0.5   # Hz si Ambient > Set 
F_LED_ALRM = 4.0   # Hz si Ambient > Set + 3 °C (alarme)
BUZZ_FREQ  = 2000

pot = ADC(Pin(PIN_POT))
led = Pin(PIN_LED, Pin.OUT); led.value(0)
buz = PWM(Pin(PIN_BUZZ)); buz.duty_u16(0)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)   # 100 kHz
lcd = GroveRGBLCD(i2c, cols=16, rows=2)             # RGB ignoré si absent
probe = dht.DHT11(Pin(PIN_DHT))

def map_pot_to_cons(v):
    c = CONS_MIN + (v / 65535.0) * (CONS_MAX - CONS_MIN)
    c = max(CONS_MIN, min(CONS_MAX, c))
    return float(int(c * 10) / 10)  # 1 décimale

def read_dht():
        probe.measure()
        return float(probe.temperature())

def show(cons, t, alarm):
    lcd.clear()
    # ligne 1 
    line1 = "Set:{:>5.1f}C".format(cons)
    if alarm and len(line1) <= 10:
        line1 += " ALARM"
    lcd.move_to(0, 0); lcd.putstr(line1[:16])

    # ligne 2 
    line2 = "Ambient:{:>6.1f}C".format(t)
    lcd.move_to(0, 1); lcd.putstr(line2[:16])

def buz_on(on):
    if on:
        buz.freq(BUZZ_FREQ); buz.duty_u16(32768)
    else:
        buz.duty_u16(0)

class Blinker:
    def __init__(self, pin):
        self.pin = pin
        self.active = False
        self.next = ticks_ms()
        self.half = 1000
    def set_freq(self, hz):
        self.active = True
        if hz < 0.1: hz = 0.1
        period = int(1000 / hz)
        self.half = max(50, period // 2)
    def off(self):
        self.active = False
        self.pin.value(0)  # force LED éteinte
    def tick(self, now):
        if not self.active:
            return
        if ticks_diff(now, self.next) >= 0:
            self.pin.value(1 - self.pin.value())
            self.next = now + self.half

blink = Blinker(led)

def main():
    last_ms = 0
    cons = map_pot_to_cons(pot.read_u16())
    last_temp = read_dht()
    if last_temp is None:
        last_temp = 0.0  # valeur de départ si 1ère mesure échoue
    alarm = False
    above = False
    show(cons, last_temp, alarm=False)

    while True:
        now = ticks_ms()
        cons = map_pot_to_cons(pot.read_u16())

        # lecture DHT environ chaque seconde
        if ticks_diff(now, last_ms) >= 1000:
            last_ms = now
            t = read_dht()
            if t is not None:
                last_temp = t  # mémorise la dernière valeur valide

            # logique LED 
            alarm = (last_temp > cons + DELTA_AL)
            above = (last_temp > cons) and not alarm

            # mise à jour LCD
            show(cons, last_temp, alarm)

            # sorties
            if alarm:
                buz_on(True)
                blink.set_freq(F_LED_ALRM)   # clignote rapide
            elif above:
                buz_on(False)
                blink.set_freq(F_LED_NORM)   # clignote lent
            else:
                # Set > Ambient -> on coupe clignotement et buzzer
                buz_on(False)
                blink.off()

        blink.tick(now)

if __name__ == "__main__":
    main()
