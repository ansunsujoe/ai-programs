import symbols

# Add a newly proposed pattern to the pattern memory
def proposePattern(array, start, length, patternCache):

    # Create a new pattern entry
    newPatternEntry = {
        "pattern": array[start:start+length],
        "strength": 0
    }

    # Add the pattern to memory
    patternCache.append(newPatternEntry)

# def identifyPatterns(array, patternCache):
    