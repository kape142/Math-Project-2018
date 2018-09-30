from rocketscience.orbit import *
from rocketscience.animation import *
from rocketscience.saturn_v import *

start_time = time.time()
resolution = 15
imagescaling = 20

orbit = OrbitSatellite(Gkonstant, AstronomicalBody(masseJorda, radiusJorda, posisjonJorda, fartJorda),
                       AstronomicalBody(masseManen, radiusManen, posisjonManen, fartManen), tol=5e-14)

animate_two_bodies_3d(orbit, imagescaling, resolution, radiusJorda, radiusManen, posisjonManen[0]/1.5,
                      86400, seconds=28, filnavn="test3", angle=(30, 90), movie=False)
