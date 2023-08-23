import matplotlib.pyplot as plt

def plot(xs, ys, labels, axis_labels= ['', ''], title = ''):
    for i in range(max(len(xs), len(ys))):
        plt.plot(xs[i],ys[i], label=labels[i])
    plt.title(title), plt.xlabel(axis_labels[0]), plt.ylabel(axis_labels[1])
    plt.legend()
    plt.show()

def plot_performance(xs, ys, labels, axis_labels= ['', ''], title = ''):
    for i in range(max(len(xs), len(ys))):
        plt.plot(xs[i],ys[i], label=labels[i])
    plt.title(title), plt.xlabel(axis_labels[0]), plt.ylabel(axis_labels[1])
    plt.legend(), plt.xlim(0, 101), plt.ylim(50, 100)
    plt.show()