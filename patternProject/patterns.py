import numeric_matching as nm

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
continuation = nm.identifyPattern(numbers, predictionNums)
if continuation != []:
    print("A continuation is: " + " ".join([str(x) for x in continuation]))
    print("Pattern found")
else:
    print("A continuation does not exist. A pattern could not be found!")