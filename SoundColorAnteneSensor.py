import time
import RPi.GPIO as GPIO
import socket
from rpi_ws281x import *

#UltraschallSensor
GPIO_TRIGGER = 11
GPIO_ECHO = 13

#LED strip Case configuration:
LED_COUNT      = 9              # Number of LED pixels.
LED_PIN        = 23             # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10             # DMA channel to use for generating signal (try 10)         Was macht das?
LED_BRIGHTNESS = 40             # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0              # set to '1' for GPIOs 13, 19, 41, 45 or 53

#LED strip Antenne configuration:
LED_COUNT_2      = 9              # Number of LED pixels.
LED_PIN_2        = 18             # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ_2    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA_2        = 10             # DMA channel to use for generating signal (try 10)         Was macht das?
LED_BRIGHTNESS_2 = 40             # Set to 0 for darkest and 255 for brightest
LED_INVERT_2     = False          # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL_2    = 0              # set to '1' for GPIOs 13, 19, 41, 45 or 53
LEDAntenne       = 1
LEDAntenneAlt    = 0

#Distanzwert mitteln
Distanz = 0
MDistanz = 0
Median = [0,0,0,0,0,0,0,0,0] #Liste für Median

#Farbberechnung aus Distanz
MAX = 60            #MAXimale Entfernung
X=0                 #Gemessene Entfernung
Stg = (255*6)/MAX   #Steigung/Konstante
Farbe = [0,0,0]     #Liste mit RGB Komponenten

#Tonfrequenzberechnung
HighTon = 52 #c''
LowTon = 28 #c
Tonindex =28
Ton=440

def setup ():
   GPIO.setmode(GPIO.BOARD)                                #GPIO Modus (BOARD / BCM)
   GPIO.setup(GPIO_TRIGGER, GPIO.OUT)                      #Richtung der GPIO-Pins festlegen (IN / OUT)
   GPIO.setup(GPIO_ECHO, GPIO.IN)

def distanz():
    global Distanz
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

    Distanz = round(float((TimeElapsed * 34300) / 2),0)  # Daraus Entfernung berechnen (c=34300 cm/s und nur eine Strecke)

    return Distanz

def MDistanz():
        global Median
        global Distanz

        for i in range(0,9):
            distanz()
            Median[i] = Distanz
            time.sleep(0.001)
        Median = sorted(Median)
        MDistanz= round((Median[4]),2)

        return MDistanz

def Frequenz(Distanz):
    global Ton
    global Tonindex
    #n = int(-float((HighTon-LowTon)/MAX)*Distanz+HighTon) #höchster Ton unten
    n = int(float((HighTon-LowTon)/MAX)*Distanz+LowTon) #tiefster Ton unten
    if n < LowTon:
        Tonindex = LowTon
    elif n <= HighTon:
        Tonindex = n
    else:
        Tonindex = HighTon
    Frequenz = round(2**((Tonindex-49)/12)*440,3)
    Ton = Frequenz
    return Frequenz

def send_Frequenz_to_pure_Data():
    global Ton
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    message = str(Ton) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))

def showColor(strip, color):                     #LED Streifen an machen in color
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def showColorAntenne(strip2, color):                     #LED Streifen an machen in color
    for i in range(0,LEDAntenne):
        strip2.setPixelColor(i, color)
        strip2.show()

def LEDoff (strip, color):
    if LEDAntenneAlt > LEDAntenne:
        X= LEDAntenne
        for i in range (X,LED_COUNT_2):
            strip.setPixelColor(i, color)
            strip.show()

def Red():                                  #Festlegung des Rotwerts aus Entfernung
    if X <= 1/6*MAX:
        Farbe[0]=255
    elif X <= 2/6*MAX:
        Farbe[0]= int(-Stg*X+Stg*(2/6)*MAX)
    elif  X <= 4/6*MAX:
        Farbe[0] = 0
    elif X <= 5/6*MAX:
        Farbe[0] = int(Stg*X-Stg*(4/6)*MAX)
    else:
        Farbe[0]=255

def Green():                                #Festlegung des Grünwerts aus Entfernung
    if X <= 1/6*MAX:
        Farbe[1]=int(Stg*X)
    elif X <= 3/6*MAX:
        Farbe[1]= 255
    elif  X <= 4/6*MAX:
        Farbe[1] = int(-Stg*X+Stg*(4/6)*MAX)
    else:
        Farbe[1]=0

def Blue():                                 #Festlegung des Blauwerts aus Entfernung
    if X <= 2/6*MAX:
        Farbe[2]= 0
    elif X <= 3/6*MAX:
        Farbe[2]= int(Stg*X-Stg*(2/6)*MAX)
    elif  X <= 5/6*MAX:
        Farbe[2] = 255
    elif X <= 6/6*MAX:
        Farbe[2] = int(-Stg*X+Stg*(6/6)*MAX)
    else:
        Farbe[2]=0

def set_Color (X):
    global Farbe
    if X <= 0:                                          #näher als 5 dran Licht = Rot
        Farbe = [255,0,0]
    elif X <= MAX:                                      #Farbe aus Funktionen
        Red()
        Green()
        Blue()
    else:                                               #Farbe lassen und Meldung raus geben
        print("zu weit weg")
    showColor(strip, Color(Farbe[0],Farbe[1],Farbe[2]))


setup()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)        #Strip inizieren
strip.begin()
print ('Press Ctrl-C to quit.')

try:
    while True:                                             # Mainloop
        X= MDistanz()-5
        Frequenz(X)                             # das -5 da es in zu nah am Sensor merkwürdig Schwank und so quasi erst ab 5cm Entfernung anfängt
        send_Frequenz_to_pure_Data()
        set_Color(X)
        LEDAntenne = int(round((Tonindex-LowTon+1)*(LED_COUNT_2/(HighTon-LowTon+1)),0))
        LEDoff(strip2, Color(0,0,0))
        showColorAntenne(strip2, Color(Farbe[0],Farbe[1],Farbe[2]))
        LEDAntenneAlt=LEDAntenne
        print(Tonindex, Ton)

except KeyboardInterrupt:
    showColor(strip, Color(0,0,0))                          #Licht aus
    GPIO.cleanup()



