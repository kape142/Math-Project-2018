from rocketscience.orbit import *


rakettKrefter = 10000
vx = 300
vy = 400
v = 500

deg = np.tan(vx/vy)
rkx = np.cos(deg)*rakettKrefter
rky = np.sin(deg)*rakettKrefter

print(rakettKrefter)
print(rkx)
print(rky)
print(np.sqrt(rkx*rkx+rky*rky))