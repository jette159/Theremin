import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state1 = GPIO.input(38)
    input_state2 = GPIO.input(36)
    if input_state1 == False and input_state2 === True:
        print ("1")
    elif input_state1 == True and input_state2 == False:
        print ("2")
    elif input_state1 == False and input_state2 == False:
        print ("3")
    else:
        print ("Chaos!")
    time.sleep(0.2)
