import numpy as np


def tetthet(h):
    # troposfæren
    if h < 11000:
        T = 288.19 - 0.00649 * h
        p = 101.29 * (T / 288.08) ** 5.256
    # Nedre stratosfære
    if h > 11000 & h < 25000:
        T = 216.69
        p = 127.76 * np.exp(-0.000157 * h)
    # Øvre stratosfære
    if h > 25000:
        T = 141.94 + 0.00299 * h
        p = 2.488 * (T / 216.6) ** -11.388
    return p / T


# CD er aerodynamisk egenskap, h er høyde, A er areal gitt et tverrsnit og v e fart.
def luftmotstand(cd, h, A, v):
    return 0.5 * cd * tetthet(h) * A * v ** 2
