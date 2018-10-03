from rocketscience.rungekutta import RungeKuttaFehlberg54
import numpy as np
import matplotlib.pyplot as plt
import pstats
import time


def F1(Y):
    M = np.array([[1, 3],
                  [2, 2]])
    res = np.ones(3)
    res[1:3] = M.dot(Y[1:3])
    return res


def F2(Y):
    M = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [0, 1, 0]])
    res = np.ones(4)
    res[1:4] = M.dot(Y[1:4]) + np.array([0, 0, 1])
    return res


def EF1(t):
    return 3 * np.exp(-t) + 2 * np.exp(4*t), -2 * np.exp(-t) + 2 * np.exp(4*t)


def EF2(t):
    ye1 = (np.exp(t) - np.exp(-t) - 2) / 2
    ye2 = (np.exp(t) + np.exp(-t) - 2) / 2
    ye3 = (np.exp(t) - np.exp(-t)) / 2
    return ye1, ye2, ye3


def example1(tol, pr):
    W = np.array([0, 5, 0])

    h = 0.1
    tEnd = 1.0
    rkf54 = RungeKuttaFehlberg54(F1, len(W), h, tol)

    while W[0] < tEnd:
        W, E = rkf54.safeStep(W)

    rkf54.setStepLength(tEnd - W[0])
    W, E = rkf54.step(W)

    if not pr:
        return W,E

    (y1, y2) = W[1:]
    ye1, ye2 = EF1(tEnd)
    print("funnet: ", y1, y2)
    print("eksakt: ", ye1, ye2)
    print("forskjell: ", y1 - ye1, y2 - ye2)
    print("funnet feil: ", E)


def example2(tol, pr):
    W = np.array([0, 0, 0, 0])
    h = 0.1
    tEnd = 1.0
    rkf54 = RungeKuttaFehlberg54(F2, len(W), h, tol)

    while W[0] < tEnd:
        W, E = rkf54.safeStep(W)

    rkf54.setStepLength(tEnd - W[0])
    W, E = rkf54.step(W)

    if not pr:
        return W, E

    (y1, y2, y3) = W[1:]
    ye1, ye2, ye3 = EF2(tEnd)
    print("funnet: ", y1, y2, y3)
    print("eksakt: ", ye1, ye2, ye3)
    print("forskjell: ", y1 - ye1, y2 - ye2, y3 - ye3)
    print("funnet feil: ", E)


example1(05e-14, True)
print("\n")
example2(05e-14, True)
print("\n")

tol = []
time_y = []
for i in range(15):
    exp = 10**(-(i))
    t0 = time.time()
    example2(exp ,False)
    t1 = time.time()
    tol.append(exp)
    time_y.append(t1-t0)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.semilogx(tol, time_y)
ax.axhline(y=10**(-2), color='r')
ax.set_ylabel("Tid (s)")
ax.set_xlabel("Toleranse")
plt.show()

print(tol)

