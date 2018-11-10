#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import time
from rpi_ws281x import *
import argparse
 
#GPIO Pins zuweisen
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

def setup ():
    #GPIO Modus (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)
    #Richtung der GPIO-Pins festlegen (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
def setColor(strip, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
      
 


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



       

a = 255
b = 128
c = 0

distance = distanz()

if distance <=5:
    Farbe = [a,c,c]
elif distance <=10:
    Farbe = [a,b,c]
elif distance <=15:
    Farbe = [a,a,c]
elif distance <=20:
    Farbe = [b,a,c]
elif distance <=25:
    Farbe = [c,a,c]
elif distance <=30:
    Farbe = [c,a,b]
elif distance <=35:
    Farbe = [c,a,a]
elif distance <=40:
    Farbe = [c,b,a]
elif distance <=45:
    Farbe = [c,c,a]
elif distance <=50:
    Farbe = [b,c,a]
elif distance <=55:
    Farbe = [a,c,a]
elif distance <=60:
    Farbe = [a,c,b]
else:
    Farbe = [c,c,c]
    print ("Fehler")
print(Farbe)

    
   
 
            
         


setup()   
if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    print ('Press Ctrl-C to quit.')
    try:
        while True:
            abstand = distanz()
            print ("Gemessene Entfernung = %.1f cm" % abstand)
            time.sleep(1)
            setColor(strip, Color(Farbe[0],Farbe[1],Farbe[2]))  
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
        GPIO.cleanup()