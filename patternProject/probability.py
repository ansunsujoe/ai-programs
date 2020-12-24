import math

# The sigmoid function
def sigmoid(value):
    return 1 / (1 + math.exp(-value))

if __name__ == "__main__":
    print(sigmoid(0))

def euclideanDistance(arr1, arr2):
    # Arrays must be of the same length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of the same length")
    # Sum the squares of the distances
    distance = 0
    for i in range(len(arr1)):
        distance += (arr2[i] - arr1[i]) ** 2
    # Return the square root
    return math.sqrt(distance)
    