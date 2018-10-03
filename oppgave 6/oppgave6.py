from rocketscience.orbit import *
from rocketscience.animation import *
from rocketscience.saturn_v import *

start_time = time.time()
resolution = 10
imagescaling = 1


def orbit_creator(a):
    return OrbitRocket(Gkonstant, AstronomicalBody(masseJorda, radiusJorda, posisjonJorda, fartJorda),
                       AstronomicalBody(masse, radiusManen, [radiusJorda, 0], [0, 0], a, kutt_motor(168+360+287)),
                       tol=5e-17, h=0.01, adjust_pitch=True, to_the_moon=False)


graph_rocket_path(orbit_creator(0), 5, 12000)
graph_all_rocket_angles(orbit_creator, 5, 10000, [90, 180], 5)

animate_two_bodies_3d(orbit_creator(0), imagescaling, resolution, radiusJorda, radiusManen / 10, radiusJorda,
                      stepsize=1, steps_per_frame=8, seconds=24, filnavn="test", angle=(10, 0),
                      colors=("green", "red"), movie=True)

# kommenter ut noen av metodene for å ikke kjøre alle etter hverandre
