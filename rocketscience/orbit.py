from numpy import sqrt
from rocketscience.rungekutta import RungeKuttaFehlberg54
from rocketscience.saturn_v import *
from rocketscience.astronomical_body import AstronomicalBody

import numpy as np


class OrbitSatellite:
    """

    Orbit Class
    For calculations concerning one massive body and a satellite, artificial or natural

    init_state is [t0,x0,vx0,y0,vx0],
    where (x0,y0) is the initial position
    , (vx0,vy0) is the initial velocity
    and t0 is the initial time
    """

    def __init__(self,
                 g=1,
                 planet=AstronomicalBody(1, 1, [0, 0], [0, 0], 0),
                 satellite=AstronomicalBody(1, 1, [0, 0], [0, 0], 0),
                 h=0.01,
                 tol=5e-14):
        self.grav_const = g
        self.satellite = satellite
        self.planet = planet
        self.time = 0
        self.h = h
        self.tol = tol

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        return self.satellite.pos

    """def energy(self):
        x = self.state[1]
        y = self.state[3]
        vx = self.state[2]
        vy = self.state[4]
        m1 = self.mPlanet
        m2 = self.mSol
        G = self.GravConst
        U = -G * m1 * m2 / sqrt(x ** 2 + y ** 2)
        K = m1 * (vx ** 2 + vy ** 2) / 2
        return K + U
    """

    def step(self, h):
        """Uses the Runge Kutta Fehlberg method to calculate the new state after h seconds."""

        state = self.satellite.state()
        state[0] = self.time
        W = state
        tEnd = W[0] + h

        rkf54 = RungeKuttaFehlberg54(self.ydot, 5, self.h, self.tol)

        while W[0] < tEnd:
            W, E = rkf54.safeStep(W)

        rkf54.setStepLength(tEnd - W[0])
        W, E = rkf54.step(W)
        self.satellite.set_state(W)
        self.time = W[0]
        # print(self.time, ": ", self.satellite.data((radiusJorda, 0)))

    def ydot(self, x):
        gm2 = self.grav_const * self.planet.mass

        px2 = 0
        py2 = 0
        px1 = x[1]
        py1 = x[3]
        vx1 = x[2]
        vy1 = x[4]
        dist = sqrt((px2 - px1) ** 2 + (py2 - py1) ** 2)
        z = np.zeros(5)
        z[0] = 1
        z[1] = vx1
        z[2] = (gm2 * (px2 - px1)) / (dist ** 3)
        z[3] = vy1
        z[4] = (gm2 * (py2 - py1)) / (dist ** 3)
        return z


class OrbitRocket:
    """

    Orbit Class
    For calculations concerning one massive body and a satellite, artificial or natural

    init_state is [t0,x0,vx0,y0,vx0],
    where (x0,y0) is the initial position
    , (vx0,vy0) is the initial velocity
    and t0 is the initial time
    """

    def __init__(self,
                 g=1,
                 planet=AstronomicalBody(1, 1, [0, 0], [0, 0]),
                 rocket=AstronomicalBody(1, 1, [0, 0], [0, 0]),
                 h=0.01,
                 tol=5e-14):
        self.grav_const = g
        self.planet = planet
        self.rocket = rocket
        self.time = 0
        self.h = h
        self.tol = tol

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        return self.rocket.pos

    """def energy(self):
        x = self.state[1]
        y = self.state[3]
        vx = self.state[2]
        vy = self.state[4]
        m1 = self.mPlanet
        m2 = self.mSol
        G = self.GravConst
        U = -G * m1 * m2 / sqrt(x ** 2 + y ** 2)
        K = m1 * (vx ** 2 + vy ** 2) / 2
        return K + U
    """

    def step(self, h):
        """Uses the Runge Kutta Fehlberg method to calculate the new state after h seconds."""

        state = self.rocket.state()
        state[0] = self.time
        W = state
        tEnd = W[0] + h

        rkf54 = RungeKuttaFehlberg54(self.ydot, 5, self.h, self.tol)
        counter = 0
        while W[0] < tEnd:
            W, E = rkf54.safeStep(W)
            counter += 1
            if counter > 1000:
                print("broken")
                break

        rkf54.setStepLength(tEnd - W[0])
        W, E = rkf54.step(W)
        self.rocket.set_state(W)
        self.time = W[0]
        print(self.time, ": ", self.rocket.data((radiusJorda, 0)))
        # print("(%.2f,%.2f)" % (self.rocket.pos_x()-radiusJorda, self.rocket.pos_y()))

    def ydot(self, x):
        gm2 = self.grav_const * self.planet.mass

        px2 = 0
        py2 = 0
        t = x[0]
        px1 = x[1]
        py1 = x[3]
        vx1 = x[2]
        vy1 = x[4]
        dist = sqrt((px2 - px1) ** 2 + (py2 - py1) ** 2)
        h = dist - radiusJorda
        rakettkrefter = self.rocket.propulsion(h, t, vy1)

        ax, ay = self.rocket.angle_decomp()
        rkx = ax * rakettkrefter
        rky = ay * rakettkrefter
        # print(t, rkx, ((gm2 * (px2 - px1)) / (dist ** 3)), rky, ((gm2 * (py2 - py1)) / (dist ** 3)))
        z = np.zeros(5)
        z[0] = 1
        z[1] = vx1
        z[2] = rkx + ((gm2 * (px2 - px1)) / (dist ** 3))  # massen til raketten skal både ganges inn og deles på
        z[3] = vy1
        z[4] = rky + ((gm2 * (py2 - py1)) / (dist ** 3))
        return z
