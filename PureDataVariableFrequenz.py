import socket
Frequenz = input("Entfernung")
s = socket.socket()
host = socket.gethostname()
port = 3000
s.connect((host, port))
message = Frequenz + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
s.send(message.encode('utf-8'))



