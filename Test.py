a = 255
b = 128
c = 0

distance = int(input("Entfernung"))

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
