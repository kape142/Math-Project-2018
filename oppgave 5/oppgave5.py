from rocketscience.orbit import *
from rocketscience.animation import *
from rocketscience.saturn_v import *

start_time = time.time()
resolution = 10
imagescaling = 1


def orbit_creator(a):
    return OrbitRocket(Gkonstant, AstronomicalBody(masseJorda, radiusJorda, posisjonJorda, fartJorda),
                       AstronomicalBody(masse, radiusManen, [radiusJorda, 0], [0, 0], a, total_kraft_oppover),
                       tol=5e-17, h=0.01, adjust_pitch=False, to_the_moon=False)


graph_rocket_path(orbit_creator(90), 5, 8000)
animate_two_bodies_3d(orbit_creator(0), imagescaling, resolution, radiusJorda, radiusManen / 10, radiusJorda * 1.1,
                      stepsize=1, steps_per_frame=5, seconds=27,
                      filnavn="Oppskytning 3", colors=("green", "red"), angle=[0, 0], movie=True)

# kommenter ut noen av metodene for å ikke kjøre alle etter hverandre
