import numpy as np
Cd = 0.75

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


# CD er aerodynamisk egenskap, h er høyde, A er areal gitt et tverrsnit og v e fart.
def luftmotstand(h, A, v):
    return 0.5 * Cd * tetthet(h) * A * v ** 2
