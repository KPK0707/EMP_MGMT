# Original function in a hypothetical library
def calculate(a, b):
    return a + b

# Monkey patch to add logging
original_calculate = calculate  # Store original function

def patched_calculate(a, b):
    print(f"Calling calculate with {a} and {b}")
    result = original_calculate(a, b)
    print(f"calculate returned {result}")
    return result

# Replace the original function with the patched version
calculate = patched_calculate

# Calling the monkey-patched function
calculate(5, 3)
