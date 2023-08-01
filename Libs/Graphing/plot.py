import matplotlib.pyplot as plt

def plot(xs, ys, labels, axis_labels= ['', ''], title = ''):
    for i in range(max(len(xs), len(ys))):
        plt.plot(xs[i],ys[i], label=labels[i])
        plt.title(title), plt.xlabel(axis_labels[0]), plt.ylabel(axis_labels[1])
        plt.show()