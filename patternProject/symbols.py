# For each unique symbol, come up with a value for it
def parseSymbolArray(array):
    # Initialize variables
    uniqueValues = sorted(set(array))
    dictionary = {}

    # Create the dictionary
    for i in range(len(uniqueValues)):
        dictionary[i + 1] = uniqueValues[i]

    # Find the new array based on this dictionary
    numericalArray = []
    for x in array:
        numericalArray.append(dictionary[x])
    
    # Return the dictionary
    return dictionary, numericalArray

def testTheDictionary():
    dictionary, numericalArray = parseSymbolArray(['x', 'y', 'z', 'w', 'n', 'x', 'y', 'w', 'x', 'z'])
    print(dictionary)
    print(numericalArray)

if __name__ == "__main__":
    testTheDictionary()