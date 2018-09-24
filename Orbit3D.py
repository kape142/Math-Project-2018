from numpy import sqrt
import time
from RungeKuttaFehlberg import RungeKuttaFehlberg54

import numpy as np
import scipy.integrate as integrate

import matplotlib.pyplot as plot
import matplotlib.animation as animation
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import axes3d
import matplotlib.image as mpimg


class Orbit:
    """

    Orbit Class

    init_state is [t0,x0,vx0,y0,vx0],
    where (x0,y0) is the initial position
    , (vx0,vy0) is the initial velocity
    and t0 is the initial time
    """

    def __init__(self,
                 init_state,
                 G=1,
                 m1=1,
                 m2=3,
                 h=0.01,
                 tol=5e-14):
        self.GravConst = G
        self.mPlanet = m1
        self.mSol = m2
        self.state = np.asarray(init_state, dtype='float')
        self.h = h
        self.tol = tol

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        x = self.state[1]
        y = self.state[3]
        return x, y

    def energy(self):
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

    def time_elapsed(self):
        return self.state[0]

    def step(self, h):
        """Uses the trapes method to calculate the new state after h seconds."""

        W = self.state
        tEnd = W[0]+h

        rkf54 = RungeKuttaFehlberg54(self.ydot, 5, self.h, self.tol)

        while W[0] < tEnd:
            W, E = rkf54.safeStep(W)

        rkf54.setStepLength(tEnd - W[0])
        W, E = rkf54.step(W)
        self.state = W

    def ydot(self, x):
        G = self.GravConst
        m2 = self.mSol
        Gm2 = G * m2

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
        z[2] = (Gm2 * (px2 - px1)) / (dist ** 3)
        z[3] = vy1
        z[4] = (Gm2 * (py2 - py1)) / (dist ** 3)
        return z


def circle(x, y, size, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = size * np.outer(np.cos(u), np.sin(v)) + x
    y = size * np.outer(np.sin(u), np.sin(v)) + y
    z = size * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z


def main():
    start_time = time.time()
    # make an Orbit instance
    orbit = Orbit([0.0, 0.0, 1.2, 2.0, 0.0])
    dt = 1. / 15  # 30 frames per second

    room_size = 3
    # The figure is set
    fig = plot.figure()
    axes = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim3d=(-room_size, room_size),
                           ylim3d=(-room_size, room_size), zlim3d=(-room_size, room_size), projection='3d')

    x, y, z = circle(0, 0, 1)
    x1, y1, z1 = circle(0, 0, 0.3)
    ball1 = axes.plot_surface(x, y, z, color='green')  # A green planet
    ball2 = axes.plot_surface(x1, y1, z1, color="gray")  # A yellow sun

    # time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes, s='0')
    # energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes, s='0')

    def animate(i):
        """perform animation step"""
        orbit.step(dt)
        axes.clear()
        xs, ys = orbit.position()
        x, y, z = circle(0, 0, 0.7)
        x1, y1, z1 = circle(xs, ys, 0.3)
        ball1 = axes.plot_surface(x, y, z, color="green")  # circle(x, y, 10))
        ball2 = axes.plot_surface(x1, y1, z1, color="gray")
        axes.set_xlim3d(-room_size, room_size)
        axes.set_ylim3d(-room_size, room_size)
        axes.set_zlim3d(-room_size, room_size)
        # line2.set_data([0.0, 0.0])
        # time_text.set_text('time = %.1f' % orbit.time_elapsed())
        # energy_text.set_text('energy = %.3f J' % orbit.energy())
        return ball1, ball2  # , time_text, energy_text

    # choose the interval based on dt and the time to animate one step
    # Take the time for one call of the animate.
    t0 = time.time()
    animate(0)
    t1 = time.time()

    delay = 1000 * dt - (t1 - t0)

    anim = animation.FuncAnimation(fig,  # figure to plot in
                                   animate,  # function that is called on each frame
                                   frames=300,  # total number of frames
                                   interval=delay,  # time to wait between each frame.
                                   repeat=False,
                                   blit=True
                                   )

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save('orbit.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    end_time = time.time()
    print("Rendering time: %.2fs" % float(end_time-start_time))


if __name__ == '__main__':
    main()
