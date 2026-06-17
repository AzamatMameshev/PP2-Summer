# Example 1
def add(a, b):
    return a + b

x = add(5, 3)
print(x)


# Example 2
def min_val(a, b):
    return min(a, b)

print(min_val(10, 4))


# Example 3
def both(a, b):
    return a + b, a * b

s, m = both(2, 3)
print(s, m)