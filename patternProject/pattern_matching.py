import array_manip as am

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
    print(str(scaledArray))
    return scaledArray
    

def identifyPattern(numbers, predictionNums):
    # If the array has only 1 number, then we have failed to find a pattern
    # This is the base case
    if len(numbers) <= 1:
        return []
    elif am.allNumsEqual(numbers):
        return numbers

    # Calculate the change-in arrays and scale down
    additionArray, multArray = am.changeIn(numbers)
    print(additionArray)
    if identifyPattern(additionArray, predictionNums) != []:
        return scaleUpChanges(numbers, additionArray, "add")
    elif multArray != [] and identifyPattern(multArray, predictionNums) != []:
        return scaleUpChanges(numbers, additionArray, "mult")
    else:
        return []