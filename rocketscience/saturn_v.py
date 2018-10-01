import matplotlib.pyplot as plt
import numpy as np
import math as m

Gkonstant = 6.674e-11
masseJorda = 5.9736e24
masseManen = 7.3477e22
radiusJorda = 6371e3
radiusManen = 1737.10e3
fartJorda = [0.0, 0.0]
fartManen = [0.0, 1022.0]
rotasjonJorda = 0.4651e3
posisjonJorda = [0.0, 0.0]
posisjonManen = [384399e3, 0.0]
Cd = 0.75
G = 9.81


def tetthet(h):
    # troposfæren
    if h < 11000:
        T = 288.19 - 0.00649 * h
        p = 101.29 * (T / 288.08) ** 5.256
    # Nedre stratosfære
    elif 11000 < h < 25000:
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

    # Trinn 1 og 2 har samme dimeter
    elif t < 529:
        return m.pi * 5.05 * 5.05
    else:
        return m.pi * 3.3 * 3.3


# CD er aerodynamisk egenskap, h er høyde, A er areal gitt et tverrsnit og v e fart.
def luftmotstand(h, t, v):
    return 0.5 * Cd * tetthet(h) * Area(t) * v * v


tidskonstanttrinn1til2 = 169
tidskonstanttrinn2til3 = 529


# y funksjoner representerer funksjoner for endring av masse i de ulike trinnen: 1,2 og 3
def masse_trinn_1(t):
    return 2.970e6 - 1.285e4 * t


def masse_trinn_2(t):
    return 6.800e5 - 1.267e3 * t


def masse_trinn_3(t):
    return 1.838e5 - 219.0 * t


# De deriverte av massen (brukt i skyvekraften)
masse_derivert_trinn_1 = -12_850
masse_derivert_trinn_2 = -1_267
masse_derivert_trinn_3 = -219


# Farten til eksos-gass i hvert trinn basert på tiden
def eksosFart(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return 2732
    elif t < 529:
        return 4058
    elif t < 1029:
        return 4566
    else:
        return 0

# Farten til eksos-gass i hvert trinn
# v_1 = 2.732*10**3
# v_2 = 4.058*10**3
# v_3 = 4.566*10**3


def masse(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return masse_trinn_1(t)
    elif t < tidskonstanttrinn2til3:
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
    elif t < tidskonstanttrinn2til3:
        return masse_derivert_trinn_2
    elif t < 1029:
        return masse_derivert_trinn_3
    return 0


def SkyvekraftRakketmotor(t):  # F=-deriverte av m * fart eksos
    return -1 * masse_derivert(t) * eksosFart(t)


def F(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return 3.510e7
    elif t < 529:
        return 5.141e6
    elif t < 1029:
        return 1.000e6
    else:
        return 0


def total_kraft_oppover(h, t, v):
    return total_kraft_oppover_kort(h, t, v, 1e9)


def kutt_motor(tid):
    return lambda h, t, v: total_kraft_oppover_kort(h, t, v, tid)


def total_kraft_oppover_kort(h, t, v, tid):
    if t > tid:
        return 0
    return (SkyvekraftRakketmotor(t) - luftmotstand(h, t, v)) / masse(t)


if __name__ == "__main__":
    y, x, y1, x1 = [], [], [], []
    for i in range(0, 1200):
        y.append(masse(i))
        x.append(i)
        y1.append(SkyvekraftRakketmotor(i)/masse(i))
        x1.append(i)

    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(x, y)
    ax.set_ylabel("Masse (kg)")
    ax.set_xlabel("Tid (s)")

    ax1 = fig.add_subplot(212)
    ax1.plot(x1, y1)
    ax1.set_ylabel("Akselerasjon (F)")
    ax1.set_xlabel("Tid (s)")
    plt.show()


# Kilde Sauer
def biseksjons_metode(funksjon, intervall, toleranse):
    a = intervall[0]
    b = intervall[1]
    while (b - a) / 2 > toleranse:
        c = (a + b) / 2
        if funksjon(c) == 0:
            return [a, b]
        if funksjon(a) * funksjon(c) < 0:
            b = c
        else:
            a = c
    return [a, b]
