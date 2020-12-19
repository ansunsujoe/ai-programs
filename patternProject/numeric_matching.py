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
    print(str(changes) + " -> " + str(scaledArray))
    return scaledArray
    

def identifyPattern(numbers, predictionNums):
    # If the array has only 1 number, then we have failed to find a pattern
    # This is the base case
    if len(numbers) <= 1:
        return []
    elif am.allNumsEqual(numbers):
        return am.resizeEqualArray(numbers, predictionNums)

    # Calculate the change-in arrays and scale up
    additionArray, multArray = am.changeIn(numbers)
    print(additionArray)

    # Scaled up addition array
    newAddChangesArray = identifyPattern(additionArray, predictionNums)
    if newAddChangesArray != []:
        return scaleUpChanges(numbers, newAddChangesArray, "add")

    # If not, then scaled up multiplication array
    newMultChangesArray = identifyPattern(multArray, predictionNums)
    if multArray != [] and newMultChangesArray != []:
        return scaleUpChanges(numbers, newMultChangesArray, "mult")
    
    # If neither method worked, then we failed
    return []