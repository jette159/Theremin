import time
from rpi_ws281x import *
import argparse

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

def setColor(strip, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()


def Red():
    if X <= 1/12*Max:
        Farbe[0]=255
    elif X <= 3/12*Max:
        Farbe[0]= int(-Stg*X+Stg*(1/4)*Max)
    elif  X <= 9/12*Max:
        Farbe[0] = 0
    elif X <= 11/12*Max:
        Farbe[0] = int(Stg*X-Stg*(3/4)*Max)
    else:
        Farbe[0]=255

def Green():
    if X <= 2/12*Max:
        Farbe[1]=int(Stg*X)
    elif X <= 5/12*Max:
        Farbe[1]= 255
    elif  X <= 7/12*Max:
        Farbe[1] = int(-Stg*X+Stg*(7/12)*Max)
    else:
        Farbe[1]=0

def Blue():
    if X <= 4/12*Max:
        Farbe[2]= 0
    elif X <= 6/12*Max:
        Farbe[0]= int(Stg*X-Stg*(1/3)*Max)
    elif  X <= 9/12*Max:
        Farbe[0] = 255
    elif X <= 11/12*Max:
        Farbe[0] = int(-Stg*X+Stg*(11/12)*Max)
    else:
        Farbe[0]=0



if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    print ('Press Ctrl-C to quit.')

    try:

        while True:
            X = int(round(float(input("Entfernung")),0))
            if X <= Max:
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

