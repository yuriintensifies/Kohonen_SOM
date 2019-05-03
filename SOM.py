import networkx as nx
import numpy as np
import csv
from process import strtoflt

def neighborhood(index, radius):
    neighbors = []
    row = index[0]
    col = index[1]
    for i in range(height):
        for j in range(width):
            dist = np.sqrt((i - row)**2 + (j - col)**2)
            if dist < radius:
                neighbors.append(((i, j), dist))
    return neighbors

def scorepoints(Weights, point):
    Scores = np.zeros((height, width))
    for n, attribute in enumerate(Weights):
        Scores = np.array(Scores + np.square(attribute - point[n]))
    bestmatch = (np.argmin(Scores) // width, np.argmin(Scores) % width)
    return Scores, bestmatch

def visualize(labels, data, dimensions):
    w = dimensions[0]
    h = dimensions[1]
    graph = nx.Graph()
    np.zeros((w, h))
    graph.add_nodes_from()

def main():
    data = []
    with open('data.csv') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        for row, line in enumerate(creader):
            data.append(list(line))
    dataset = strtoflt(data)
    dataset = np.array(dataset, dtype=float)
    global width
    width = 15
    global height
    height = 15
    radius = 7.0
    iterations = 400
    learning_rate = 1
    shrink_rate = 0.2
    param = len(dataset[0])
    Weights = np.random.rand(param, height, width)
    for k in range(iterations):
        for point in dataset:
            Scores, bestmatch = scorepoints(Weights, point)
            for neighbor in neighborhood(bestmatch, radius):
                coord = neighbor[0]
                dist = neighbor[1]
                if dist != 0:
                    penalty = dist/radius
                else: penalty = 0
                Weights[:, coord[0], coord[1]] += learning_rate*(1-penalty)*(point - Weights[:, coord[0], coord[1]])

        radius = shrink_rate*(radius**(k/iterations))
        learning_rate = shrink_rate*(learning_rate**(k/iterations))

    results = []
    for n, point in enumerate(dataset):
        _, bestmatch = scorepoints(Weights, point)
        results.append(bestmatch)
    labels = []
    with open('labels.csv') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        for row in creader:
            labels.append(row)

    output = dict(zip(labels[0], results))


    divergence = [[0 for i in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            for n, input in enumerate(Weights):
                if i < height-1:
                    divergence[i][j] += (input[i + 1][j] - input[i][j]) ** 2
                    if j < width-1:
                        divergence[i][j] += (input[i + 1][j + 1] - input[i][j]) ** 2
                    if j > 0:
                        divergence[i][j] += (input[i + 1][j - 1] - input[i][j]) ** 2
                if j < width-1:
                    divergence[i][j] += (input[i][j + 1] - input[i][j]) ** 2
                    if i > 0:
                        divergence[i][j] += (input[i - 1][j + 1] - input[i][j]) ** 2
                if i > 0:
                    divergence[i][j] += (input[i - 1][j] - input[i][j]) ** 2
                    if j > 0:
                        divergence[i][j] += (input[i - 1][j - 1] - input[i][j]) ** 2
                if j > 0:
                    divergence[i][j] += (input[i][j - 1] - input[i][j]) ** 2




    with open('divergence.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(divergence)

    #visualize(labels, results, (height, width))

    with open('results.csv', 'w', newline='') as out:
        dwriter = csv.writer(out)
        dwriter.writerow(list(output.keys()))
        dwriter.writerow(output[i][0] for i in output.keys())
        dwriter.writerow(output[i][1] for i in output.keys())

if __name__ == "__main__":
    main()