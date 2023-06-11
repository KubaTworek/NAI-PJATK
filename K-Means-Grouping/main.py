import csv
import math
import random


def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x, y, *z = map(float, row)
            data.append((x, y, *z))
    return data


def euclidean_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += (p1[i] - p2[i]) ** 2
    return math.sqrt(distance)


def kmeans(data, k):
    centroids = random.sample(data, k)
    groups = [[] for _ in range(k)]

    while True:
        for point in data:
            distances = [euclidean_distance(point, centroid) for centroid in centroids]
            group_index = distances.index(min(distances))
            groups[group_index].append(point)

        new_centroids = []
        for group in groups:
            if group:
                new_centroids.append(tuple(sum(point[i] for point in group) / len(group) for i in range(len(point))))
            else:
                new_centroids.append(centroids[groups.index(group)])

        if new_centroids == centroids:
            break

        sse = 0
        for group, centroid in zip(groups, centroids):
            sse += sum(euclidean_distance(point, centroid) ** 2 for point in group)

        for i, group in enumerate(groups):
            print(f'Grupa {i + 1}: {len(group)} punktów')
        print(f'Sumaryczna suma kwadratów odległości wewnątrz klastrów: {sse:.2f}')
        print('---------------------------------------')

        centroids = new_centroids
        groups = [[] for _ in range(k)]


data = load_data('data.csv')
kmeans(data, 3)