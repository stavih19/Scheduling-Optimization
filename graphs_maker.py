import csv
import matplotlib.pyplot as plt


def make_plot():
    x = []
    y1 = []
    y2 = []

    with open("Outputs/output_soldiers.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            x.append(int(line[2]))
            y1.append(float(line[0]))
            y2.append(float(line[4]))
    plt.plot(x, y1)
    plt.xlabel("number of soldiers")
    plt.ylabel("run time")
    plt.title("runtime by number of soldiers")
    plt.savefig('Graphs/runtime by number of soldiers.png')
    plt.show()

    plt.plot(x, y2)
    plt.xlabel("number of soldiers")
    plt.ylabel("limit")
    plt.title("limit by number of soldiers")
    plt.savefig('Graphs/limit by number of soldiers.png')
    plt.show()

    ###########

    x = []
    y1 = []
    y2 = []

    with open("Outputs/output_tasks.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        fields = next(reader)
        for line in reader:
            x.append(int(line[3]))
            y1.append(float(line[0]))
            y2.append(float(line[4]))
    plt.plot(x, y1)
    plt.xlabel("number of tasks")
    plt.ylabel("run time")
    plt.title("runtime by number of tasks")
    plt.savefig('Graphs/runtime by number of tasks.png')
    plt.show()

    plt.plot(x, y2)
    plt.xlabel("number of soldiers")
    plt.ylabel("limit")
    plt.title("limit by number of tasks")
    plt.savefig('Graphs/limit by number of tasks.png')
    plt.show()

    a = 0


make_plot()
