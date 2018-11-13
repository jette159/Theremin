MAX = 60 #maximale Entfernung
HighTon = 52 #c''
LowTon = 28 #c

Distanz = float(input("Entfernung: "))
print(Distanz)
n = int(-float((HighTon-LowTon)/MAX)*Distanz+HighTon) #höchster Ton unten
#n = int(((HighTon-LowTon)/MAX)*Distanz+LowTon) #tiefster Ton unten
print(n)
Zwischen = float(n-49)
print(Zwischen)
Frequenz = round(2**(Zwischen/12)*440,3)
print(Frequenz)


