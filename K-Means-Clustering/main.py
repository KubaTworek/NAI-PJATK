import csv
import math
import operator
import os


# Funkcja wczytująca zbiór danych z pliku CSV
def loadDataset(filename):
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for i in range(len(dataset)):
            for j in range(4):
                dataset[i][j] = float(dataset[i][j])
            if dataset[i][4] == 'Iris-setosa':
                dataset[i][4] = 0
            elif dataset[i][4] == 'Iris-versicolor':
                dataset[i][4] = 1
            elif dataset[i][4] == 'Iris-virginica':
                dataset[i][4] = 2
    return dataset


# Funkcja obliczająca odległość między dwoma punktami
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for i in range(length):
        distance += pow((instance1[i] - instance2[i]), 2)
    return math.sqrt(distance)


# Funkcja zwracająca k najbliższych sąsiadów dla danego przypadku testowego
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for i in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[i], length)
        distances.append((trainingSet[i], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


# Funkcja dokonująca klasyfikacji dla danego przypadku testowego
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


# Funkcja obliczająca dokładność klasyfikacji dla danych testowych
def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


# Funkcja pobierająca wektor od użytkownika
def classifyNewInstance(trainingSet, k):
    while True:
        inputStr = input("Podaj wartości wektora oddzielone przecinkami: ")
        inputList = inputStr.split(',')
        testInstance = [0.0, 0.0, 0.0, 0.0, ""]
        for j in range(4):
            testInstance[j] = float(inputList[j])
        if inputList[4] == 'Iris-setosa':
            testInstance[4] = 0
        elif inputList[4] == 'Iris-versicolor':
            testInstance[4] = 1
        elif inputList[4] == 'Iris-virginica':
            testInstance[4] = 2

        # Wyszukanie k najbliższych sąsiadów
        neighbors = getNeighbors(trainingSet, testInstance, k)

        # Klasyfikacja wektora na podstawie najbliższych sąsiadów
        result = getResponse(neighbors)
        print("Klasyfikacja wektora:", result)


# Argumenty
k = 105
trainFile = os.path.join(os.path.dirname(__file__), 'trainFile.csv')
testFile = os.path.join(os.path.dirname(__file__), 'testFile.csv')

# Wczytanie zbiorów treningowego i testowego
trainingSet = loadDataset(trainFile)
testSet = loadDataset(testFile)

# Dokonanie predykcji dla każdego przypadku testowego
predictions = []
for x in range(len(testSet)):
    neighbors = getNeighbors(trainingSet, testSet[x], k)
    result = getResponse(neighbors)
    predictions.append(result)
    print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))

# Obliczenie dokładności klasyfikacji i wyświetlenie wyniku
accuracy = getAccuracy(testSet, predictions)
print('Accuracy: ' + repr(accuracy) + '%')

classifyNewInstance(trainingSet, k)
