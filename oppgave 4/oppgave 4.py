import rocketscience.saturn_v as sv
import matplotlib.pyplot as plt

if __name__ == "__main__":
    y, x, y1, x1 = [], [], [], []
    for i in range(0, 1200):
        y.append(sv.masse(i))
        x.append(i)
        y1.append(sv.SkyvekraftRakketmotor(i)/sv.masse(i))
        x1.append(i)

    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(x, y)
    ax.set_ylabel("Masse (kg)")
    ax.set_xlabel("Tid (s)")

    ax1 = fig.add_subplot(212)
    ax1.plot(x1, y1)
    ax1.set_ylabel("Akselerasjon (m/s^2)")
    ax1.set_xlabel("Tid (s)")
    plt.show()
