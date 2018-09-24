from numpy import sqrt
import time

import numpy as np
import scipy.integrate as integrate

import matplotlib.pyplot as plot
import matplotlib.animation as animation
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import axes3d
from Orbit3D import *

start_time = time.time()
resolution = 40
imagescaling = 7
Gkonstant = 6.674e-11
masseJorda = 5.9736e24
masseManen = 7.3477e22
diameterJorda = 12756.28e3 * imagescaling
diameterManen = 1737.10e3 * 2 * imagescaling
fartJorda = 0.0
fartManen = 1022
posisjonJorda = 0.0
posisjonManen = 384399e3



def krefter_g(Gkon1stant, masseJorda, masseManen, posisjonJorda, posisjonManen):
    return Gkonstant * masseManen * masseJorda * (
                (posisjonJorda - posisjonManen) / ((posisjonJorda ** 3 - posisjonManen ** 3) ** (1 / 3)))


# make an Orbit instance
orbit = Orbit([0.0, posisjonManen, 0, 0, fartManen], Gkonstant, masseManen, masseJorda, tol=5e-18)
dt = 1/30

room_size = posisjonManen
# The figure is set
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim3d=(-room_size, room_size),
                       ylim3d=(-room_size, room_size), zlim3d=(-room_size, room_size), projection='3d')

x, y, z = circle(0, 0, diameterJorda, resolution)
x1, y1, z1 = circle(posisjonManen, 0, diameterManen, resolution)
ball1 = axes.plot_surface(x, y, z, color='green')  # A green planet
ball2 = axes.plot_surface(x1, y1, z1, color="gray")  # A yellow sun


# time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes, s='0')
# energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes, s='0')


def animate(i):
    """perform animation step"""
    global orbit, dt
    orbit.step(dt*86400)
    axes.clear()
    xs, ys = orbit.position()
    x, y, z = circle(0, 0, diameterJorda, resolution)
    x1, y1, z1 = circle(xs, ys, diameterManen, resolution)
    ball1 = axes.plot_surface(x, y, z, color="green")
    ball2 = axes.plot_surface(x1, y1, z1, color="gray")
    axes.set_xlim3d(-room_size, room_size)
    axes.set_ylim3d(-room_size, room_size)
    axes.set_zlim3d(-room_size, room_size)
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
                               frames=30*28,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True
                               )

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('orbit 28 dager.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

print("Rendering time: %.2fs" % float(time.time() - start_time))
