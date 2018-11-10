import time
from rpi_ws281x import *
import RPi.GPIO as GPIO
import argparse

GPIO_TRIGGER = 11
GPIO_ECHO = 13

# LED strip configuration:
LED_COUNT      = 9      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 40     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

Max = 60            #Maximale Entfernung
X=0                 #Gemessene Entfernung
Stg = (255*6)/Max   #Steigung/Konstante
Farbe = [0,0,0]     #Liste mit RGB Komponenten

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


def setColor(strip, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()


def Red():
    if X <= 1/6*Max:
        Farbe[0]=255
    elif X <= 2/6*Max:
        Farbe[0]= int(-Stg*X+Stg*(2/6)*Max)
    elif  X <= 4/6*Max:
        Farbe[0] = 0
    elif X <= 5/6*Max:
        Farbe[0] = int(Stg*X-Stg*(4/6)*Max)
    else:
        Farbe[0]=255

def Green():
    if X <= 1/6*Max:
        Farbe[1]=int(Stg*X)
    elif X <= 3/6*Max:
        Farbe[1]= 255
    elif  X <= 4/6*Max:
        Farbe[1] = int(-Stg*X+Stg*(4/6)*Max)
    else:
        Farbe[1]=0

def Blue():
    if X <= 2/6*Max:
        Farbe[2]= 0
    elif X <= 3/6*Max:
        Farbe[2]= int(Stg*X-Stg*(2/6)*Max)
    elif  X <= 5/6*Max:
        Farbe[2] = 255
    elif X <= 6/6*Max:
        Farbe[2] = int(-Stg*X+Stg*(6/6)*Max)
    else:
        Farbe[2]=0


setup()
if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    print ('Press Ctrl-C to quit.')

    try:

        while True:
            X = int(round(float(distanz()),0))
            # X = int(round(float(input("Entfernung")),0))
            if X == 0:
                Farbe = [0,0,0]
            elif X <= Max:
                Red()
                Green()
                Blue()

                print(Farbe)

            else:
                print("zu weit weg")
            setColor(strip, Color(Farbe[0],Farbe[1],Farbe[2]))



    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

