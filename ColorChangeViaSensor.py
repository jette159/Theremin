#Bibliotheken einbinden
import time
from rpi_ws281x import *
import RPi.GPIO as GPIO

#UltraschallSensor
GPIO_TRIGGER = 11
GPIO_ECHO = 13

#LED strip configuration:
LED_COUNT      = 9              # Number of LED pixels.
LED_PIN        = 18             # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10             # DMA channel to use for generating signal (try 10)         Was macht das?
LED_BRIGHTNESS = 40             # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0              # set to '1' for GPIOs 13, 19, 41, 45 or 53



#Farbberechnung aus Distanz
Max = 60            #Maximale Entfernung
X=0                 #Gemessene Entfernung
Stg = (255*6)/Max   #Steigung/Konstante
Farbe = [0,0,0]     #Liste mit RGB Komponenten

def setup ():
   GPIO.setmode(GPIO.BOARD)                                #GPIO Modus (BOARD / BCM)
   GPIO.setup(GPIO_TRIGGER, GPIO.OUT)                      #Richtung der GPIO-Pins festlegen (IN / OUT)
   GPIO.setup(GPIO_ECHO, GPIO.IN)



def distance():
    GPIO.output(GPIO_TRIGGER, True)                     # setze Trigger auf HIGH

    time.sleep(0.00001)                                 # setze Trigger nach 0.01ms aus LOW
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()                             #Start- und Stopzeit definieren
    StopZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 0:                   # speichere Startzeit
        StartZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 1:                   # speichere Ankunftszeit
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit                  # Zeitdifferenz zwischen Start und Ankunft

    distanz = (TimeElapsed * 34300) / 2                 # Daraus Entfernung berechnen (c=34300 cm/s und nur eine Strecke)

    return distanz                                      #Distanz ausgeben


def showColor(strip, color):                     #LED Streifen an machen in color
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()


def Red():                                  #Festlegung des Rotwerts aus Entfernung
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

def Green():                                #Festlegung des Grünwerts aus Entfernung
    if X <= 1/6*Max:
        Farbe[1]=int(Stg*X)
    elif X <= 3/6*Max:
        Farbe[1]= 255
    elif  X <= 4/6*Max:
        Farbe[1] = int(-Stg*X+Stg*(4/6)*Max)
    else:
        Farbe[1]=0

def Blue():                                 #Festlegung des Blauwerts aus Entfernung
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

def setColor(Distanz):
    if Distanz <= 0:
        Farbe = [0,0,0]
    elif Distanz <= Max:
        Red()
        Green()
        Blue()
    else:
        print("zu weit weg")



setup()
if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    print ('Press Ctrl-C to quit.')

    try:

        while True:
            X = int(round(float(distance()),0))-5        # das -5 da es in zu nah am Sensor merkwürdig Schwank und so quasi erst ab 5cm Entfernung anfängt
            setColor(X)
            print (distance)
            print(Farbe)
            showColor(strip, Color(Farbe[0],Farbe[1],Farbe[2]))
            time.sleep(0.1)

    except KeyboardInterrupt:
        if args.clear:
            showColor(strip, Color(0,0,0))

