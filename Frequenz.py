MAX = 60 #maximale Entfernung
HighTon = 52 #c''
LowTon = 28 #c

Distanz = float(input("Entfernung: "))
print(Distanz)
#n = int(-float((HighTon-LowTon)/MAX)*Distanz+HighTon) #höchster Ton unten
n = int(float((HighTon-LowTon)/MAX)*Distanz+LowTon) #tiefster Ton unten
print(n)
Frequenz = round(2**((n-49)/12)*440,3)
print(Frequenz)


