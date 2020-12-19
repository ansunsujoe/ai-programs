import math

# The sigmoid function
def sigmoid(value):
    return 1 / (1 + math.exp(-value))

if __name__ == "__main__":
    print(sigmoid(0))