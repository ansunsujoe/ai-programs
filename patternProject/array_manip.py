# Change in
def changeIn(numbers):
    # Initialize arrays to store the results
    additionArray = []
    multArray = []

    # Calculate changes from one number to the next in the "pattern"
    for i in range(len(numbers) - 1):
        additionArray.append(numbers[i + 1] - numbers[i])
        try:
            multArray.append(numbers[i + 1] / numbers[i])
        except ZeroDivisionError:
            multArray = []
    
    # Return
    return additionArray, multArray

# Are all the numbers in the array equal
def allNumsEqual(numbers):
    trueNum = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] != trueNum:
            return False
    return True