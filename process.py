import numpy as np
import csv

def striplabels(data):
    labels = []
    attrib = []
    for point in data:
        labels.append(point[0])
        attrib.append(point[1:])
    return labels, attrib

def strtoflt(data):
    out = []
    for row in data:
        newrow = []
        for str in row:
            if str == '':
                newrow.append('')
                continue
            newrow.append(float(str))
        out.append(newrow)
    return out

def fillempty(data):
    avgs = [0] * len(data[0])
    counts = [0] * len(data[0])
    for row in data:
        for n, str in enumerate(row):
            if str == '':
                continue
            avgs[n] += str
            counts[n] += 1
    for i in range(len(avgs)):
        avgs[i] /= counts[i]
    for row in data:
        for n, str in enumerate(row):
            if str == '':
                row[n] = avgs[n]
    return 0

def regularize(data):
    max = []
    max = np.amax(data, axis=0)
    print(max)
    for row in data:
        for i, element in enumerate(row):
            row[i] /= max[i]
    return max



def main():
    data = []
    with open('countries.csv') as csvfile:
        creader = csv.reader(csvfile, delimiter=',')
        for row, line in enumerate(creader):
            if row == 0:
                continue
            data.append(list(line))
    labels, dataset = striplabels(data)
    dataset = strtoflt(dataset)
    fillempty(dataset)
    maximum = regularize(dataset)

    with open('data.csv', 'w', newline='') as out:
        dwriter = csv.writer(out)
        dwriter.writerows(dataset)

    with open('labels.csv', 'w', newline='') as out:
        dwriter = csv.writer(out)
        dwriter.writerow(labels)

    with open('max.csv', 'w', newline='') as out:
        dwriter = csv.writer(out)
        dwriter.writerow(maximum)


if __name__ == "__main__":
    main()




