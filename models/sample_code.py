#!/usr/bin/env python3
"""
Sample Python code with various code quality issues for testing the AI Code Mentor analyzer.
"""

def very_long_function_with_many_lines():
    """This function is intentionally long to test the analyzer's detection of long functions."""
    print("This is line 1")
    print("This is line 2")
    print("This is line 3")
    print("This is line 4")
    print("This is line 5")
    print("This is line 6")
    print("This is line 7")
    print("This is line 8")
    print("This is line 9")
    print("This is line 10")
    print("This is line 11")
    print("This is line 12")
    print("This is line 13")
    print("This is line 14")
    print("This is line 15")
    print("This is line 16")
    print("This is line 17")
    print("This is line 18")
    print("This is line 19")
    print("This is line 20")
    print("This is line 21")
    print("This is line 22")
    print("This is line 23")
    print("This is line 24")
    print("This is line 25")
    print("This is line 26")
    print("This is line 27")
    print("This is line 28")
    print("This is line 29")
    print("This is line 30")
    print("This is line 31 - exceeds the limit!")
    return "Function is too long"


def function_with_nested_loops():
    """This function has deeply nested loops to test the analyzer."""
    result = []
    
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):  # This is the 4th level - should be flagged
                    result.append(i + j + k + l)
    
    return result


def potential_infinite_loop():
    """This function has a while loop without clear exit condition."""
    i = 0
    while True:  # Should be flagged as potential infinite loop
        i += 1
        if i > 1000:  # This condition is too high to be practical
            break
    return i


def good_function():
    """This is a well-structured function that should pass all checks."""
    numbers = [1, 2, 3, 4, 5]
    squared = [n ** 2 for n in numbers]
    return sum(squared)


def complex_function_with_many_conditions():
    """This function has high cyclomatic complexity."""
    result = 0
    
    for i in range(100):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 5 == 0:
                    if i % 7 == 0:
                        result += i
                    else:
                        result -= i
                else:
                    result *= 2
            else:
                result += 1
        else:
            if i < 50:
                result += i
            else:
                result -= i
    
    return result


# Main execution
if __name__ == "__main__":
    print("Testing AI Code Mentor analyzer...")
    
    # Test each function
    print("1. Testing long function...")
    very_long_function_with_many_lines()
    
    print("2. Testing nested loops...")
    nested_result = function_with_nested_loops()
    print(f"Result length: {len(nested_result)}")
    
    print("3. Testing potential infinite loop...")
    infinite_result = potential_infinite_loop()
    print(f"Result: {infinite_result}")
    
    print("4. Testing good function...")
    good_result = good_function()
    print(f"Result: {good_result}")
    
    print("5. Testing complex function...")
    complex_result = complex_function_with_many_conditions()
    print(f"Result: {complex_result}")
    
    print("Analysis complete!") 