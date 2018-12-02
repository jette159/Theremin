import time
import RPi.GPIO as GPIO
import socket
from rpi_ws281x import *

#UltraschallSensor Frequenz
GPIO_TRIGGER_F = 11
GPIO_ECHO_F = 13

#UltraschallSensor Volume
GPIO_TRIGGER_V = 29
GPIO_ECHO_V = 31

#LED strip Case configuration:
LED_COUNT      = 9              # Number of LED pixels.
LED_PIN        = 18             # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10             # DMA channel to use for generating signal (try 10)         Was macht das?
LED_BRIGHTNESS = 40             # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False          # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0              # set to '1' for GPIOs 13, 19, 41, 45 or 53

#LED strip Antenne configuration:
LED_COUNT_2      = 34             # Number of LED pixels.
LED_PIN_2        = 21             # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ_2    = 800000         # LED signal frequency in hertz (usually 800khz)
LED_DMA_2        = 10             # DMA channel to use for generating signal (try 10)         Was macht das?
LED_BRIGHTNESS_2 = 40             # Set to 0 for darkest and 255 for brightest
LED_INVERT_2     = False          # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL_2    = 0              # set to '1' for GPIOs 13, 19, 41, 45 or 53
LEDAntenne       = 1
LEDAntenneAlt    = 0

#Distanzwert Frequenz
Distanz_F = 0
MDistanz_F = 0
Median_F = [0,0,0,0,0,0,0,0,0] #Liste für Median

#Distanzwert Volume
Distanz_V = 0
MDistanz_V = 0
Median_V = [0,0,0,0,0,0,0,0,0] #Liste für Median


#Farbberechnung aus Distanz
MAX = 47            #MAXimale Entfernung
X=0                 #Gemessene Entfernung
Stg = (255*6)/MAX   #Steigung/Konstante
Farbe = [0,0,0]     #Liste mit RGB Komponenten

#Tonfrequenzberechnung
HighTon = 52 #c''
LowTon = 28 #c
Tonindex =28
Ton=440

#Volumeberechnung
MAX_V = float(30)
Volume = 0

def setup ():
    GPIO.setmode(GPIO.BOARD)                                #GPIO Modus (BOARD / BCM)
    GPIO.setup(GPIO_TRIGGER_F, GPIO.OUT)                      #Richtung der GPIO-Pins festlegen (IN / OUT)
    GPIO.setup(GPIO_ECHO_F, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER_V, GPIO.OUT)                      #Richtung der GPIO-Pins festlegen (IN / OUT)
    GPIO.setup(GPIO_ECHO_V, GPIO.IN)

def get_distanz_F():
    global Distanz_F
    GPIO.output(GPIO_TRIGGER_F, True)                     # setze Trigger auf HIGH

    time.sleep(0.00001)                                 # setze Trigger nach 0.01ms aus LOW
    GPIO.output(GPIO_TRIGGER_F, False)

    StartZeit_F = time.time()                             #Start- und Stopzeit definieren
    StopZeit_F = time.time()

    while GPIO.input(GPIO_ECHO_F) == 0:                   # speichere Startzeit
        StartZeit_F = time.time()

    while GPIO.input(GPIO_ECHO_F) == 1:                   # speichere Ankunftszeit
        StopZeit_F = time.time()

    TimeElapsed = StopZeit_F - StartZeit_F                  # Zeitdifferenz zwischen Start und Ankunft

    Distanz_F = round(float((TimeElapsed * 34300) / 2),0)  # Daraus Entfernung berechnen (c=34300 cm/s und nur eine Strecke)

    return Distanz_F

def MDistanz_F():
    global Median_F
    global Distanz_F

    for i in range(0,9):
        get_distanz_F()
        Median_F[i] = Distanz_F
        time.sleep(0.001)
    Median_F = sorted(Median_F)
    MDistanz_F= round((Median_F[4]),2)
    MDistanz_F=MDistanz_F-5
    return MDistanz_F

def set_Frequenz(Distanz):
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

def send_Frequenz_and_Volume_to_pure_Data():
    global Ton
    global Volume
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    message = "0 " + str(Ton) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))
    print (message)
    message = "1 " + str(Volume) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))
    print (message)

def get_distanz_V():
    global Distanz_V
    GPIO.output(GPIO_TRIGGER_V, True)                     # setze Trigger auf HIGH

    time.sleep(0.00001)                                 # setze Trigger nach 0.01ms aus LOW
    GPIO.output(GPIO_TRIGGER_V, False)

    StartZeit_V = time.time()                             #Start- und Stopzeit definieren
    StopZeit_V = time.time()

    while GPIO.input(GPIO_ECHO_V) == 0:                   # speichere Startzeit
        StartZeit_V = time.time()

    while GPIO.input(GPIO_ECHO_V) == 1:                   # speichere Ankunftszeit
        StopZeit_V = time.time()

    TimeElapsed = StopZeit_V - StartZeit_V                  # Zeitdifferenz zwischen Start und Ankunft

    Distanz_V = round(float((TimeElapsed * 34300) / 2),0)  # Daraus Entfernung berechnen (c=34300 cm/s und nur eine Strecke)

    return Distanz_V

def MDistanz_V():
    global Median_V
    global Distanz_V
    for i in range(0,9):
        get_distanz_V()
        Median_V[i] = Distanz_V
        time.sleep(0.001)
    Median_V = sorted(Median_V)
    MDistanz_V= round((Median_V[4]),2)
    MDistanz_V=MDistanz_V-5
    return float(MDistanz_V)

def set_Volume(Distanz):
    global Volume
    Volume = Distanz/MAX_V #100% = 1

def showColor(strip, color):                     #LED Streifen an machen in color
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def LEDoff (strip, color):
    global LEDAntenne
    LEDAntenne = int(round((Tonindex-LowTon+1)*(LED_COUNT_2/(HighTon-LowTon+1)),0))+9
    if LEDAntenneAlt > LEDAntenne:
        X= LEDAntenne
        print(X)
        for i in range (X,LED_COUNT_2):
            strip.setPixelColor(i, color)
            strip.show()

def showColorAntenne(strip2, color):                     #LED Streifen an machen in color
    global LEDAntenneAlt
    for i in range(0,LEDAntenne):
        strip2.setPixelColor(i, color)
        strip2.show()
    LEDAntenneAlt=LEDAntenne

def Red(X):                                  #Festlegung des Rotwerts aus Entfernung
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

def Green(X):                                #Festlegung des Grünwerts aus Entfernung
    if X <= 1/6*MAX:
        Farbe[1]=int(Stg*X)
    elif X <= 3/6*MAX:
        Farbe[1]= 255
    elif  X <= 4/6*MAX:
        Farbe[1] = int(-Stg*X+Stg*(4/6)*MAX)
    else:
        Farbe[1]=0

def Blue(X):                                 #Festlegung des Blauwerts aus Entfernung
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
        Red(X)
        Green(X)
        Blue(X)
    else:                                               #Farbe lassen und Meldung raus geben
        print("zu weit weg")
    showColor(strip, Color(Farbe[0],Farbe[1],Farbe[2]))


setup()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)        #Strip inizieren
strip.begin()
strip2 = Adafruit_NeoPixel(LED_COUNT_2, LED_PIN_2, LED_FREQ_HZ_2, LED_DMA_2, LED_INVERT_2, LED_BRIGHTNESS_2, LED_CHANNEL_2)        #Strip inizieren
strip2.begin()
print ('Press Ctrl-C to quit.')

try:
    while True:                                             # Mainloop # das -5 da es in zu nah am Sensor merkwürdig Schwank und so quasi erst ab 5cm Entfernung anfängt
        final_Distanz_F= MDistanz_F()
        set_Frequenz(final_Distanz_F)
        final_Distanz_V=MDistanz_V()
        set_Volume(final_Distanz_V)
        send_Frequenz_and_Volume_to_pure_Data()
        set_Color(final_Distanz_F)
        LEDoff(strip2, Color(0,0,0))
        showColorAntenne(strip2, Color(Farbe[0],Farbe[1],Farbe[2]))


except KeyboardInterrupt:
    showColor(strip, Color(0,0,0))                          #Licht aus
    showColor(strip2, Color(0,0,0))
    GPIO.cleanup()
