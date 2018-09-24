import matplotlib.pyplot as plt
import numpy as np
import math as m

Cd = 0.75
G = 9.81

def tetthet(h):
    # troposfæren
    if h < 11000:
        T = 288.19 - 0.00649 * h
        p = 101.29 * (T / 288.08) ** 5.256
    # Nedre stratosfære
    elif h > 11000 & h < 25000:
        T = 216.69
        p = 127.76 * np.exp(-0.000157 * h)
    # Øvre stratosfære
    else:
        T = 141.94 + 0.00299 * h
        p = 2.488 * (T / 216.6) ** -11.388
    return (p / T) * 3.4855


def Area(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')

    #Trinn 1 og 2 har samme dimeter
    elif t < 529:
        return m.pi*5.05**2
    else:
        return m.pi*3.3**2

# CD er aerodynamisk egenskap, h er høyde, A er areal gitt et tverrsnit og v e fart.
def luftmotstand(h, t, v):
    return 0.5 * Cd * tetthet(h) * Area(t) * v ** 2

tidskonstanttrinn1til2 = 168
tidskonstanttrinn2til3 = 529

#y funksjoner representerer funksjoner for endring av masse i de ulike trinnen: 1,2 og 3
def masse_trinn_1(t):
    return 2.970*10**6-1.285*10**4*t

def masse_trinn_2(t):
    return 6.800*10**5-1.267*10**3*t

def masse_trinn_3(t):
    return 1.838*10**5-219.0*t

# De deriverte av massen (brukt i skyvekraften)
masse_derivert_trinn_1 = -1.285 * 10 ** 4
masse_derivert_trinn_2 = -1.267 * 10 ** 3
masse_derivert_trinn_3 = -219.0

#Farten til eksos-gass i hvert trinn basert på tiden
def eksosFart(t):
    if t > tidskonstanttrinn2til3 :
        return 4566
    if t > tidskonstanttrinn1til2:
        return 4058
    return 2732

#Farten til eksos-gass i hvert trinn
#v_1 = 2.732*10**3
#v_2 = 4.058*10**3
#v_3 = 4.566*10**3

def masse(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return masse_trinn_1(t)
    elif t < 529:
        return masse_trinn_2(t - 168)
    elif t < 1029:
        return masse_trinn_3(t - 528)
    else:
        return masse_trinn_3(500)

def masse_derivert(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < tidskonstanttrinn1til2:
        return masse_derivert_trinn_1
    elif t < 529:
        return masse_derivert_trinn_2
    return masse_derivert_trinn_3

def SkyvekraftRakketmotor(t): # F=-derriverte av m * fart eksos
    return -1*masse_derivert(t)*eksosFart(t)

def F(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return 3.510*10**7
    elif t < 529:
        return 5.141*10**6
    elif t < 1029:
        return 1.000*10**6
    else:
        return 0

def tyngdekraft_rakett(t):
    return masse(t)*G

def total_kraft_oppover(h, t, v):
    return SkyvekraftRakketmotor(t) - luftmotstand(h, t, v) - tyngdekraft_rakett(t)


if __name__ == "__main__":
    y, x, y1, x1 = [], [], [], []
    for i in range(0,1030):
        y.append(masse(i))
        x.append(i)
        y1.append(SkyvekraftRakketmotor(i))
        x1.append(i)

    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(x,y)
    ax.set_ylabel("Masse (kg)")
    ax.set_xlabel("Tid (s)")

    ax1 = fig.add_subplot(212)
    ax1.plot(x1,y1)
    ax1.set_ylabel("Skyvekraft (N)")
    ax1.set_xlabel("Tid (s)")
    plt.show()
