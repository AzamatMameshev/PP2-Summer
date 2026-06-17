# Example 1
nums = [5, 2, 9]
print(sorted(nums))


# Example 2
nums = [5, 2, 9]
print(sorted(nums, key=lambda x: -x))


# Example 3
pairs = [(1, 3), (2, 1)]
print(sorted(pairs, key=lambda x: x[1]))
