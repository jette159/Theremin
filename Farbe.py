Max = 60            #Maximale Entfernung
X=0                 #Gemessene Entfernung
Stg = (255*6)/Max   #Steigung/Konstante

Farbe = [0,0,0]     #Liste mit RGB Komponenten

X = int(round(float(input("Entfernung")),0))
def Red():
    if X <= 1/12*Max:
        Farbe[0]=255
    elif X <= 3/12*Max:
        Farbe[0]= int(-Stg*X+Stg*(1/4)*Max)
    elif  X <= 9/12*Max:
        Farbe[0] = 0
    elif X <= 11/12*Max:
        Farbe[0] = int(Stg*X-Stg*(3/4)*Max)
    else:
        Farbe[0]=255

def Green():
    if X <= 2/12*Max:
        Farbe[1]=int(Stg*X)
    elif X <= 5/12*Max:
        Farbe[1]= 255
    elif  X <= 7/12*Max:
        Farbe[1] = int(-Stg*X+Stg*(7/12)*Max)
    else:
        Farbe[1]=0

def Blue():
    if X <= 4/12*Max:
        Farbe[2]= 0
    elif X <= 6/12*Max:
        Farbe[0]= int(Stg*X-Stg*(1/3)*Max)
    elif  X <= 9/12*Max:
        Farbe[0] = 255
    elif X <= 11/12*Max:
        Farbe[0] = int(-Stg*X+Stg*(11/12)*Max)
    else:
        Farbe[0]=0


if X <= Max:
    Red()
    Green()
    Blue()

    print(Farbe)

else:
    print("zu weit weg")

#change



