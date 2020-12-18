##############
# FUNCTIONS
##############

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

# When the correct change-in values have been found for a continuation, then
# update them in the upper level of the pattern tree
def scaleUpChanges(numbers, changes, operation):
    scaledArray = []
    scaledArray.append(numbers[len(numbers) - 1])
    for i in range(len(changes)):
        # Depending on the operation, use that to calculate the new scaled changes
        if operation == "add":
            scaledArray.append(scaledArray[i] + changes[i])
        elif operation == "mult":
            scaledArray.append(scaledArray[i] * changes[i])
    # Take out the first element as that is only a helper
    scaledArray.pop(0)
    return scaledArray
    

def identifyPattern(numbers, predictionNums):
    # If the array has only 1 number, then we have failed to find a pattern
    # This is the base case
    if len(numbers) <= 1:
        return []
    elif allNumsEqual(numbers):
        return numbers

    # Calculate the change-in arrays and scale down
    additionArray, multArray = changeIn(numbers)
    print(additionArray)
    if identifyPattern(additionArray, predictionNums) != []:
        return scaleUpChanges(numbers, additionArray, "add")
    elif multArray != [] and identifyPattern(multArray, predictionNums) != []:
        return scaleUpChanges(numbers, additionArray, "mult")
    else:
        return []

#############
# MAIN 
#############

# Get input from user
rawString = input("Enter number pattern: ")
predictionNums = 3

# Convert input to a number array
try:
    numbers = [int(x) for x in rawString.split()]
except ValueError:
    print("ERROR: Something wrong")

# Print output
print("The array is: " + " ".join([str(x) for x in numbers]))

# Try to find the pattern and print it
continuation = identifyPattern(numbers, predictionNums)
if continuation != []:
    print("A continuation is: " + " ".join([str(x) for x in continuation]))
    print("Pattern found")

