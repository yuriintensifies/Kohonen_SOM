import networkx as nx
import csv
import numpy as np
from process import strtoflt
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.colors

def main():
    labels = []
    data = []
    with open('results.csv') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        for row, line in enumerate(creader):
            if row == 0:
                labels = line
            else:
                val = []
                for element in line:
                    val.append(element)
                data.append(val)

    data = strtoflt(data)

    """
    y = data[0]
    x = data[1]

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    for i, text in enumerate(labels):
        ax.annotate(text, (x[i], y[i]))
    plt.show()
    """

    ct = [['' for i in range(15)] for i in range(15)]
    data = np.transpose(data)
    for n, coord in enumerate(data):
        if ct[int(coord[0])][int(coord[1])] == '':
            ct[int(coord[0])][int(coord[1])] = labels[n]
            continue
        ct[int(coord[0])][int(coord[1])] = ct[int(coord[0])][int(coord[1])]+', '+labels[n]

    #table = plt.table(cellText=ct, rowLabels=rows, colLabels=columns)
    #plt.show()
    #graph = nx.grid_2d_graph(20, 20)
    #G = nx.petersen_graph()
    #plt.subplot(121)
    #nx.draw_planar(graph, with_labels=True, font_weight='bold')

    trace = go.Table(
        cells=dict(values=ct)
    )

    data2 = [trace]
    py.plot(data2, filename='table.html')



if __name__ == "__main__":
    main()




