import random


def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    n = int(lines[0])
    distances = [[0] * n for _ in range(n)]

    for line in lines[1:]:
        v1, v2, d = map(int, line.split())
        distances[v1][v2] = d
        distances[v2][v1] = d

    return n, distances


def calculate_total_distance(route, distances):
    total_distance = 0
    for i in range(len(route) - 1):
        v1 = route[i]
        v2 = route[i + 1]
        total_distance += distances[v1][v2]
    return total_distance


def hill_climbing(n, distances):
    current_route = list(range(n))
    random.shuffle(current_route)
    current_distance = calculate_total_distance(current_route, distances)

    best_route = current_route[:]
    best_distance = current_distance

    iterations = 0

    while True:
        neighbors = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                neighbor = current_route[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)

        found_better_neighbor = False

        for neighbor in neighbors:
            neighbor_distance = calculate_total_distance(neighbor, distances)
            if neighbor_distance < current_distance:
                current_route = neighbor[:]
                current_distance = neighbor_distance
                found_better_neighbor = True
                if current_distance < best_distance:
                    best_route = current_route[:]
                    best_distance = current_distance

        iterations += 1
        print(f"Iteration: {iterations}, Best Distance: {best_distance}")

        if not found_better_neighbor:
            break

    return best_route, best_distance


def main():
    file_path = 'data.csv'
    n, distances = read_data(file_path)
    best_route, best_distance = hill_climbing(n, distances)
    print(f"Best Route: {''.join(map(str, best_route))}")
    print(f"Total Distance: {best_distance}")


if __name__ == '__main__':
    main()
