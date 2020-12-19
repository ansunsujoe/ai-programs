import symbols

# Add a newly proposed pattern to the pattern memory
def proposePattern(array, start, length, patternMem):

    # Create a new pattern entry
    newPatternEntry = {
        "pattern": array[start:start+length],
        "strength": 0
    }

    # Add the pattern to memory
    patternMem.append(newPatternEntry)

