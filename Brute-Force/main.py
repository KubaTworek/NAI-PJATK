def combinations(n, k):
    """
    Generuje kombinacje n-elementowe o długości k.
    """
    combinations = []
    stack = []
    x = 0

    while True:
        if len(stack) == k:
            combinations.append(stack[:])

        if x < n:
            stack.append(x)
            x += 1
        elif stack:
            x = stack.pop() + 1
        else:
            break

    return combinations


def brute_force_knapsack(capacity, values, weights):
    num_items = len(values)
    best_value = 0
    best_combination = ()

    for i in range(1, num_items + 1):
        combinations_list = combinations(num_items, i)

        for combination in combinations_list:
            current_value = sum([values[j] for j in combination])
            current_weight = sum([weights[j] for j in combination])

            if current_weight <= capacity and current_value > best_value:
                best_value = current_value
                best_combination = combination

    result = [0] * num_items
    for index in best_combination:
        result[index] = 1

    return result


def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    capacity = int(lines[0].strip())
    values = list(map(int, lines[1].split(',')))
    weights = list(map(int, lines[2].split(',')))

    return capacity, values, weights


def main():
    file_path = 'data.csv'
    capacity, values, weights = read_data(file_path)

    result = brute_force_knapsack(capacity, values, weights)
    print("Najlepszy wektor:", result)


if __name__ == '__main__':
    main()
