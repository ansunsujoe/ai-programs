# For each unique symbol, come up with a value for it
def parseSymbolArray(array):
    # Initialize variables
    uniqueValues = list(sorted(set(array)))
    dictionary = {}

    # Create the dictionary
    for i in range(len(uniqueValues)):
        dictionary[uniqueValues[i]] = i + 1

    # Find the new array based on this dictionary
    numericalArray = []
    for x in array:
        numericalArray.append(dictionary[x])
    
    # Return the dictionary
    return dictionary, numericalArray

# Return array from numbers back to symbols using the dictionary
def arrNumToSymbols(array, dictionary):
    newArray = []
    for num in array:
        newArray.append(list(dictionary.keys())[num - 1])
    return newArray

# Test method - serves as the main
def testTheDictionary():
    dictionary, numericalArray = parseSymbolArray(['x', 'y', 'z', 'w', 'n', 'x', 'y', 'w', 'x', 'z'])
    print(dictionary)
    print(numericalArray)
    print(arrNumToSymbols(numericalArray, dictionary))

if __name__ == "__main__":
    testTheDictionary()