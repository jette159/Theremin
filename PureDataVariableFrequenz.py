import time
import RPi.GPIO as GPIO
import socket

MAX = 60 #maximale Entfernung
HighTon = 52 #c''
LowTon = 28 #c
Ton=440

#UltraschallSensor
GPIO_TRIGGER = 11
GPIO_ECHO = 13

MDistanz = 0
Median = [0,0,0,0,0,0,0,0,0] #Liste für Median

def setup ():
   GPIO.setmode(GPIO.BOARD)                                #GPIO Modus (BOARD / BCM)
   GPIO.setup(GPIO_TRIGGER, GPIO.OUT)                      #Richtung der GPIO-Pins festlegen (IN / OUT)
   GPIO.setup(GPIO_ECHO, GPIO.IN)

def distanz():
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

    distanz = int(round(float((TimeElapsed * 34300) / 2),0))  # Daraus Entfernung berechnen (c=34300 cm/s und nur eine Strecke)

    return distanz                                      #Distanz ausgeben

def MDistanz():
        global Median
        for i in range(0,9):
            Median[i] = distanz()
            time.sleep(0.001)
        Median = sorted(Median)
        MDistanz= round((Median[4]),2)
        return MDistanz

def Frequenz(Distanz):
    #n = int(-float((HighTon-LowTon)/MAX)*Distanz+HighTon) #höchster Ton unten
    n = int(float((HighTon-LowTon)/MAX)*Distanz+LowTon) #tiefster Ton unten
    Frequenz = round(2**((n-49)/12)*440,3)
    return Frequenz

def send_Frequenz_to_pure_Data():
    global Ton
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    message = str(Ton) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))

setup()
try:
    while True:                                             # Mainloop
        X = MDistanz() # das -5 da es in zu nah am Sensor merkwürdig Schwank und so quasi erst ab 5cm Entfernung anfängt
        Ton=Frequenz(X)
        send_Frequenz_to_pure_Data()
        print(Ton)

except KeyboardInterrupt:
    GPIO.cleanup()






