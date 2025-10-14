from machine import Pin, PWM, ADC
from utime import ticks_ms, ticks_diff


pot = ADC(Pin(27))   
buzzer = PWM(Pin(28))     

C4, D4, E4, F4, G4, A4, B4 = 262, 294, 330, 349, 392, 440, 494      # attribution des notes à une fréquences (récupéré sur internet)
C5, D5, E5, F5, G5, A5 = 523, 587, 659, 698, 784, 880
REST = 0

notes = [
    C4, C4, D4, C4, F4, E4,
    C4, C4, D4, C4, G4, F4,
    C4, C4, C5, A4, F4, E4, D4,                                     # méodie joyeux anniversaire (récupéré sur internet)
    B4, B4, A4, F4, G4, F4
]

volume = 0
note_index = 0

last_pot_time = 0
last_note_time = 0

while True:                                                         # boucle infinie
    now = ticks_ms()
    volume = pot.read_u16()
    print(volume)

    if ticks_diff(now, last_pot_time) >= 10:                        # lit la valeur du potentiomètre toutes les 10 ms
        buzzer.duty_u16(volume)
        last_pot_time = now

    if ticks_diff(now, last_note_time) >= 500:                      # change de note toutes les 500 ms
        freq = notes[note_index]

        if freq == REST or volume <= 500 or volume >= 50000:
            buzzer.duty_u16(0)                                      # silence si pot est inférieur à 500 (résistance interne) ou supérieur à 50 000 (sature)
        else:
            buzzer.freq(freq)

        note_index = (note_index + 1) % len(notes)                  # change de note et reviens à 0 quand la liste est finie
        last_note_time = now

