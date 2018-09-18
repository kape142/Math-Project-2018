import matplotlib.pyplot as plt

#y funksjoner representerer funksjoner for endring av masse i de ulike trinnen: 1,2 og 3
def y_1(t):
    return 2.970*10**6-1.285*10**4*t


def y_2(t):
    return 6.800*10**5-1.267*10**3*t


def y_3(t):
    return 1.838*10**5-219.0*t

#Farten til eksos-gass i hvert trinn
v_1 = 2.732*10**3
v_2 = 4.058*10**3
v_3 = 4.566*10**3

def m(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return y_1(t)
    elif t < 529:
        return y_2(t-168)
    elif t < 1029:
        return y_3(t-528)
    else:
        return y_3(500)

def F(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 169:
        return 3.510*10**7
    elif t < 529:
        return 5.141*10**6
    elif t < 1029:
        return 1.000*10**6
    else:
        return 0

if __name__ == "__main__":
    y, x, y1, x1 = [], [], [], []
    for i in range(0,1030):
        y.append(m(i))
        x.append(i)
        y1.append(F(i))
        x1.append(i)

    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(x,y)
    ax.set_ylabel("Masse (kg)")
    ax.set_xlabel("Tid (s)")

    ax1 = fig.add_subplot(212)
    ax1.plot(x1,y1)
    ax1.set_ylabel("Skyvekraft (N)")
    ax1.set_xlabel("Tid (s)")
    plt.show()
