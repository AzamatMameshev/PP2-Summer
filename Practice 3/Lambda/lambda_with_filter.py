# Example 1
nums = [1, 2, 3, 4]
print(list(filter(lambda x: x % 2 == 0, nums)))


# Example 2
nums = [-2, 5, -1]
print(list(filter(lambda x: x > 0, nums)))


# Example 3
words = ["hi", "", "ok"]
print(list(filter(lambda s: len(s) > 0, words)))