from rocketscience.orbit import *
from rocketscience.animation import *
from rocketscience.saturn_v import *

start_time = time.time()
resolution = 10
imagescaling = 1


def orbit_creator(a):
    return OrbitRocket(Gkonstant, AstronomicalBody(masseJorda, radiusJorda, posisjonJorda, fartJorda),
                       AstronomicalBody(masse, radiusManen, [0, radiusJorda], [0, 0], a, kutt_motor(1e9)),
                       tol=5e-17, h=0.001)


graph_rocket_path(orbit_creator(47), 40, 10000)
# graph_all_rocket_angles(orbit_creator, 10, 10000, [20, 45], 1)

# animate_two_bodies_3d(orbit, imagescaling, resolution, radiusJorda, radiusManen / 3, radiusJorda * 1.3, stepsize=150,
# seconds=30, filnavn="test", colors=("green", "red"), movie=True)
