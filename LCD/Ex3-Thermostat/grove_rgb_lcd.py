# grove_rgb_lcd.py — auto-détection RGB (texte à 0x3E, RGB à 0x62 si présent)
from time import sleep_ms

_ADDR_TEXT_DEFAULT = 0x3E
_ADDR_RGB_DEFAULT  = 0x62
_CMD = 0x80
_DAT = 0x40

class GroveRGBLCD:
    def __init__(self, i2c, cols=16, rows=2, addr_text=_ADDR_TEXT_DEFAULT, addr_rgb=_ADDR_RGB_DEFAULT, freq_safe=False):
        # freq_safe=True si tu veux forcer 100 kHz ailleurs (tu peux gérer ça hors driver)
        self.i2c = i2c
        self.cols = cols
        self.rows = rows
        self.addr_text = addr_text
        self.addr_rgb  = addr_rgb
        # auto-détecter la présence du chip RGB
        try:
            found = i2c.scan()
        except Exception:
            found = []
        self.has_rgb = (self.addr_rgb in found)
        self._init_text()
        if self.has_rgb:
            self._init_rgb()

    # --- bas niveau texte ---
    def _cmd(self, c):
        self.i2c.writeto(self.addr_text, bytes([_CMD, c]))

    def _data(self, d):
        self.i2c.writeto(self.addr_text, bytes([_DAT, d]))

    # --- init texte ---
    def _init_text(self):
        sleep_ms(50)
        self._cmd(0x38)   # 8-bit, 2 lignes, 5x8
        self._cmd(0x06)   # entry mode: inc, no shift
        self._cmd(0x0C)   # display on, cursor off, blink off
        self.clear()

    # --- bas niveau RGB ---
    def _rgb_write(self, reg, val):
        # si pas de RGB détecté, on ne fait rien
        if not self.has_rgb: 
            return
        self.i2c.writeto_mem(self.addr_rgb, reg, bytes([val]))

    def _init_rgb(self):
        # PCA9633-like
        self._rgb_write(0x00, 0x00)  # MODE1
        self._rgb_write(0x01, 0x00)  # MODE2
        self._rgb_write(0x08, 0xAA)  # LEDOUT: PWM all
        self.set_rgb(255, 255, 255)  # blanc

    # --- API publique ---
    def clear(self):
        self._cmd(0x01); sleep_ms(2)

    def home(self):
        self._cmd(0x02); sleep_ms(2)

    def move_to(self, col, row):
        col = max(0, min(self.cols - 1, col))
        row = max(0, min(self.rows - 1, row))
        base = [0x00, 0x40, 0x00 + self.cols, 0x40 + self.cols]
        self._cmd(0x80 | (base[row] + col))

    def putstr(self, s):
        for ch in str(s):
            self._data(ord(ch))

    def set_rgb(self, r, g, b):
        if not self.has_rgb:
            return  # Pas de chip RGB : on ignore
        # Ordre registres souvent B,G,R
        self._rgb_write(0x02, b & 0xFF)
        self._rgb_write(0x03, g & 0xFF)
        self._rgb_write(0x04, r & 0xFF)

    def backlight_off(self):
        self.set_rgb(0, 0, 0)

    def backlight_on(self):
        self.set_rgb(255, 255, 255)
