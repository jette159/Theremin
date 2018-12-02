import socket
Ton=0
Volume=0
def send_Frequenz_and_Volume_to_pure_Data():
    global Ton
    global Volume
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    message = "0 " + str(Ton) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))
    message = "1 " + str(Volume) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))

while True:
    Ton=input("Ton")
    Volume=input("Volume")
    send_Frequenz_and_Volume_to_pure_Data()
