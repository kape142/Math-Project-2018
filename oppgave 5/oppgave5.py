from rocketscience.orbit import *
from rocketscience.animation import *
from rocketscience.saturn_v import *

start_time = time.time()
resolution = 10
imagescaling = 1

orbit = OrbitRocket(Gkonstant, AstronomicalBody(masseJorda, radiusJorda, posisjonJorda, fartJorda),
                    AstronomicalBody(0, radiusManen, [radiusJorda, 0], [0, 0], 0, total_kraft_oppover), tol=5e-11)

animate_two_bodies_3d(orbit, imagescaling, resolution, radiusJorda, radiusManen / 3, radiusJorda * 1.3, stepsize=90,
                      seconds=40, filnavn="test", colors=("green", "red"), movie=True)

