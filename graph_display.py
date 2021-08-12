import matplotlib.pyplot as plt
import pylab as pl


def process_values(tasks, single_values, all_values):
    y_single_first = []
    y_single_middle = []
    y_single_last = []

    y_all_first = []
    y_all_middle = []
    y_all_last = []

    print(single_values)
    print(all_values)

    for i in range(len(single_values)):
        if i % 3 == 0:
            y_single_first.append(single_values[i])
            y_all_first.append(all_values[i])
        elif i % 3 == 1:
            y_single_middle.append(single_values[i])
            y_all_middle.append(all_values[i])
        elif i % 3 == 2:
            y_single_last.append(single_values[i])
            y_all_last.append(all_values[i])

    print(tasks)
    print(y_single_first)
    print(y_single_middle)
    print(y_single_last)

    fig, axs = plt.subplots(2)
    fig.suptitle('Single & All solider measurement')

    axs[0].plot(tasks, y_single_first)
    axs[0].plot(tasks, y_single_middle)
    axs[0].plot(tasks, y_single_last)

    axs[1].plot(tasks, y_all_first)
    axs[1].plot(tasks, y_all_middle)
    axs[1].plot(tasks, y_all_last)

    plt.ylim(ymin=0)
    plt.legend()
    plt.show()

