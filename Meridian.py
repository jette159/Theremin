#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import statistics

#GPIO Pins zuweisen
GPIO_TRIGGER = 11
GPIO_ECHO = 13

Median = [] #Liste für Median
Entfernung = 0

def setup ():
    #GPIO Modus (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)
    #Richtung der GPIO-Pins festlegen (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz

def Zentralwert():
        for i in (0,8):
        Median[i] = distanz()
    print (Median)
    Entfernung = statistics.median(Median)


setup()
if __name__ == '__main__':
    try:
        while True:
            Zentralwert()
            print (Entfernung)
            time.sleep(0.5)

        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
